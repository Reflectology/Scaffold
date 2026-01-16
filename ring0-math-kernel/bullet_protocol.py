#!/usr/bin/env python3
"""
Bullet Consensus Protocol for Reflectology

Direct Python port of bullet.tla / bullet.c
Implements lightweight consensus for distributed ring deployment.

TLA+ Spec: ring9/docs/docs/bullet.tla
C Reference: ring0/ring0/bullet.c

Safety Invariants:
- OneLeader: At most one leader per term
- LogConsistency: All 2a messages in same term have same value
"""

import struct
import socket
import threading
import queue
import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Callable, Any, Tuple
from enum import IntEnum
from collections import defaultdict

# =============================================================================
# MESSAGE TYPES (per bullet.tla)
# =============================================================================

class MsgType(IntEnum):
    """Message types from TLA+ spec: {"1a","1b","2a","2b"}"""
    MSG_1A = 0x1A  # Phase 1a: Prepare request
    MSG_1B = 0x1B  # Phase 1b: Promise response
    MSG_2A = 0x2A  # Phase 2a: Accept request (leader -> quorum)
    MSG_2B = 0x2B  # Phase 2b: Accepted response

class Role(IntEnum):
    """Acceptor roles from TLA+ spec"""
    FOLLOWER = 0
    CANDIDATE = 1
    LEADER = 2

# =============================================================================
# DATA STRUCTURES (aligned with bullet.tla TypeOK)
# =============================================================================

@dataclass
class BulletMessage:
    """
    Network message per TLA+ spec:
    msgs ⊆ [type: {"1a","1b","2a","2b"}, sender: Acceptor, term: Nat, value: Seq(Value)]
    """
    msg_type: MsgType
    sender: int  # Acceptor ID
    term: int
    values: List[Any] = field(default_factory=list)
    checksum: str = ""
    
    def serialize(self) -> bytes:
        """Binary wire format: [type:1][sender:1][term:4][vlen:2][values:n][checksum:8]"""
        payload = json.dumps(self.values).encode('utf-8')
        self.checksum = hashlib.sha256(payload).hexdigest()[:8]
        header = struct.pack(">BBIH", self.msg_type, self.sender, self.term, len(payload))
        return header + payload + self.checksum.encode('utf-8')
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'BulletMessage':
        """Parse message from wire format"""
        if len(data) < 8:
            raise ValueError("Message too short")
        msg_type, sender, term, vlen = struct.unpack(">BBIH", data[:8])
        payload = data[8:8+vlen]
        checksum = data[8+vlen:8+vlen+8].decode('utf-8')
        values = json.loads(payload.decode('utf-8')) if payload else []
        return cls(MsgType(msg_type), sender, term, values, checksum)
    
    def verify(self) -> bool:
        """Verify message integrity"""
        payload = json.dumps(self.values).encode('utf-8')
        return hashlib.sha256(payload).hexdigest()[:8] == self.checksum


@dataclass
class Acceptor:
    """
    Acceptor state per TLA+ spec:
    - state ∈ [Acceptor → {"Follower","Candidate","Leader"}]
    - votes ∈ [Acceptor → Nat]
    - logs ∈ [Acceptor → Seq(Value)]
    """
    id: int
    role: Role = Role.FOLLOWER
    votes: int = 0  # Last term voted for
    log: List[Any] = field(default_factory=list)
    
    def clone(self) -> 'Acceptor':
        return Acceptor(self.id, self.role, self.votes, self.log.copy())


@dataclass
class BulletState:
    """
    Global system state per TLA+ spec:
    VARIABLES state, bullet, logs, term, votes, quorum, msgs
    """
    n: int  # Number of acceptors
    acceptors: Dict[int, Acceptor] = field(default_factory=dict)
    bullet: int = 0  # Current leader ID
    term: int = 0
    quorum: Set[int] = field(default_factory=set)
    msgs: List[BulletMessage] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.acceptors:
            for i in range(self.n):
                self.acceptors[i] = Acceptor(id=i)
            # Initial leader (CHOOSE a ∈ Acceptor : TRUE)
            self.acceptors[0].role = Role.LEADER
            self.bullet = 0
            # Majority quorum: ceil(n/2)
            self.quorum = set(range((self.n // 2) + 1))


# =============================================================================
# ACTIONS (per bullet.tla Next)
# =============================================================================

class BulletActions:
    """
    TLA+ Actions:
    Next == PromoteCandidate \\/ LeaderElection \\/ LogReplication 
            \\/ MessageBroadcast \\/ MagicBulletPass
    """
    
    @staticmethod
    def promote_candidate(state: BulletState, acceptor_id: int) -> bool:
        r"""
        PromoteCandidate ==
          /\ exists a in Acceptor : state[a] = "Follower" /\ state' = [state EXCEPT ![a] = "Candidate"]
          /\ UNCHANGED <<bullet, logs, term, votes, quorum, msgs>>
        """
        if acceptor_id not in state.acceptors:
            return False
        acc = state.acceptors[acceptor_id]
        if acc.role != Role.FOLLOWER:
            return False
        acc.role = Role.CANDIDATE
        return True
    
    @staticmethod
    def leader_election(state: BulletState, candidate_id: int) -> bool:
        """LeaderElection: Candidate with quorum votes becomes leader, term increments."""
        if candidate_id not in state.acceptors:
            return False
        acc = state.acceptors[candidate_id]
        if acc.role != Role.CANDIDATE:
            return False
        # Guard: ∀ q ∈ quorum : votes[q] = term
        for q in state.quorum:
            if state.acceptors[q].votes != state.term:
                return False
        # Demote current leader
        for a in state.acceptors.values():
            if a.role == Role.LEADER:
                a.role = Role.FOLLOWER
        # Elect new leader
        acc.role = Role.LEADER
        state.bullet = candidate_id
        state.term += 1
        return True
    
    @staticmethod
    def log_replication(state: BulletState) -> bool:
        """LogReplication: Leader copies log to quorum and emits 2a message."""
        leader = state.acceptors.get(state.bullet)
        if not leader or leader.role != Role.LEADER:
            return False
        # Copy leader log to quorum
        for q in state.quorum:
            state.acceptors[q].log = leader.log.copy()
        # Emit 2a message
        msg = BulletMessage(
            msg_type=MsgType.MSG_2A,
            sender=state.bullet,
            term=state.term,
            values=leader.log.copy()
        )
        state.msgs.append(msg)
        return True
    
    @staticmethod
    def message_broadcast(state: BulletState) -> bool:
        """MessageBroadcast: Remove 1a message if quorum has no leader."""
        # Check if quorum has no leader
        has_leader = any(state.acceptors[q].role == Role.LEADER for q in state.quorum)
        if has_leader:
            return False
        # Find and remove a 1a message
        for i, m in enumerate(state.msgs):
            if m.msg_type == MsgType.MSG_1A:
                state.msgs.pop(i)
                return True
        return False
    
    @staticmethod
    def magic_bullet_pass(state: BulletState, new_leader: int) -> bool:
        """MagicBulletPass: Transfer leadership to another node."""
        if new_leader not in state.acceptors:
            return False
        if new_leader == state.bullet:
            return False
        leader = state.acceptors.get(state.bullet)
        if not leader or leader.role != Role.LEADER:
            return False
        # Transfer leadership
        leader.role = Role.FOLLOWER
        state.acceptors[new_leader].role = Role.LEADER
        state.bullet = new_leader
        return True


# =============================================================================
# SAFETY INVARIANTS (per bullet.tla Safety)
# =============================================================================

class BulletInvariants:
    """Safety == OneLeader AND LogConsistency"""
    
    @staticmethod
    def one_leader(state: BulletState) -> bool:
        """OneLeader: At most one acceptor has role Leader."""
        leaders = sum(1 for a in state.acceptors.values() if a.role == Role.LEADER)
        return leaders <= 1
    
    @staticmethod
    def log_consistency(state: BulletState) -> bool:
        """LogConsistency: All 2a messages in same term have same value."""
        msgs_2a = [m for m in state.msgs if m.msg_type == MsgType.MSG_2A]
        for i, m1 in enumerate(msgs_2a):
            for m2 in msgs_2a[i+1:]:
                if m1.term == m2.term and m1.values != m2.values:
                    return False
        return True
    
    @staticmethod
    def check_safety(state: BulletState) -> Tuple[bool, str]:
        """Check all safety invariants"""
        if not BulletInvariants.one_leader(state):
            return False, "OneLeader violated"
        if not BulletInvariants.log_consistency(state):
            return False, "LogConsistency violated"
        return True, "Safety OK"


# =============================================================================
# NETWORK TRANSPORT (lightweight TCP, no gRPC)
# =============================================================================

class BulletTransport:
    """
    Lightweight TCP transport for Bullet protocol.
    Replaces gRPC with protocol-level implementation.
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 9876):
        self.host = host
        self.port = port
        self.state: Optional[BulletState] = None
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.handlers: Dict[MsgType, Callable] = {}
        self.peers: Dict[int, Tuple[str, int]] = {}  # acceptor_id -> (host, port)
        self._recv_queue: queue.Queue = queue.Queue()
        self._server_thread: Optional[threading.Thread] = None
    
    def init_state(self, n: int, node_id: int):
        """Initialize local state for this node"""
        self.state = BulletState(n=n)
        self.node_id = node_id
    
    def add_peer(self, acceptor_id: int, host: str, port: int):
        """Register a peer acceptor"""
        self.peers[acceptor_id] = (host, port)
    
    def start_server(self) -> bool:
        """Start TCP server for receiving messages"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(32)
            self.server_socket.settimeout(1.0)
            self.running = True
            
            self._server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self._server_thread.start()
            
            print(f"✓ Bullet node {self.node_id} listening on {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ Failed to start Bullet server: {e}")
            return False
    
    def _server_loop(self):
        """Accept connections and handle messages"""
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                threading.Thread(target=self._handle_connection, args=(conn,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Server error: {e}")
    
    def _handle_connection(self, conn: socket.socket):
        """Handle a single connection"""
        try:
            # Read message length prefix (4 bytes)
            len_data = conn.recv(4)
            if len(len_data) < 4:
                return
            msg_len = struct.unpack(">I", len_data)[0]
            
            # Read message body
            data = b""
            while len(data) < msg_len:
                chunk = conn.recv(min(4096, msg_len - len(data)))
                if not chunk:
                    break
                data += chunk
            
            msg = BulletMessage.deserialize(data)
            if msg.verify():
                self._process_message(msg)
                # Send ACK
                conn.sendall(b"\x00")
            else:
                conn.sendall(b"\x01")  # NACK
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            conn.close()
    
    def _process_message(self, msg: BulletMessage):
        """Process received message according to protocol"""
        if self.state is None:
            return
        
        self.state.msgs.append(msg)
        
        if msg.msg_type == MsgType.MSG_1A:
            # Respond with 1b (promise)
            if msg.term >= self.state.acceptors[self.node_id].votes:
                self.state.acceptors[self.node_id].votes = msg.term
                resp = BulletMessage(
                    msg_type=MsgType.MSG_1B,
                    sender=self.node_id,
                    term=msg.term,
                    values=self.state.acceptors[self.node_id].log.copy()
                )
                self.send_to(msg.sender, resp)
        
        elif msg.msg_type == MsgType.MSG_2A:
            # Accept value from leader
            if msg.term >= self.state.term:
                self.state.acceptors[self.node_id].log = msg.values.copy()
                resp = BulletMessage(
                    msg_type=MsgType.MSG_2B,
                    sender=self.node_id,
                    term=msg.term,
                    values=msg.values.copy()
                )
                self.send_to(msg.sender, resp)
        
        # Invoke custom handler if registered
        handler = self.handlers.get(msg.msg_type)
        if handler:
            handler(msg)
    
    def send_to(self, acceptor_id: int, msg: BulletMessage) -> bool:
        """Send message to specific peer"""
        if acceptor_id not in self.peers:
            return False
        host, port = self.peers[acceptor_id]
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((host, port))
            data = msg.serialize()
            sock.sendall(struct.pack(">I", len(data)) + data)
            ack = sock.recv(1)
            sock.close()
            return ack == b"\x00"
        except Exception as e:
            print(f"Send to {acceptor_id} failed: {e}")
            return False
    
    def broadcast(self, msg: BulletMessage) -> int:
        """Broadcast to all peers, return success count"""
        success = 0
        for peer_id in self.peers:
            if self.send_to(peer_id, msg):
                success += 1
        return success
    
    def broadcast_to_quorum(self, msg: BulletMessage) -> bool:
        """Broadcast to quorum and wait for majority ack"""
        if self.state is None:
            return False
        success = 0
        for q in self.state.quorum:
            if q == self.node_id:
                success += 1  # Count self
                continue
            if self.send_to(q, msg):
                success += 1
        return success >= len(self.state.quorum) // 2 + 1
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()


# =============================================================================
# RING INTEGRATION (replaces ring4_network.py gRPC need)
# =============================================================================

class BulletRingBridge:
    """
    Bridge between Bullet consensus and Reflectology ring architecture.
    Provides distributed coordination without gRPC.
    """
    
    def __init__(self, node_id: int, n_nodes: int = 3):
        self.transport = BulletTransport()
        self.transport.init_state(n_nodes, node_id)
        self.node_id = node_id
        self._omega_log: List[Dict] = []  # Log of omega state changes
    
    def configure_cluster(self, peers: List[Tuple[int, str, int]]):
        """Configure cluster with peer addresses: [(id, host, port), ...]"""
        for peer_id, host, port in peers:
            if peer_id != self.node_id:
                self.transport.add_peer(peer_id, host, port)
    
    def start(self, port: int) -> bool:
        """Start this node"""
        self.transport.port = port
        return self.transport.start_server()
    
    def is_leader(self) -> bool:
        """Check if this node is the leader"""
        return self.transport.state.bullet == self.node_id
    
    def propose_omega(self, omega_data: Dict) -> bool:
        """
        Propose an omega state change through consensus.
        Only leader can propose; uses log replication.
        """
        if not self.is_leader():
            return False
        
        state = self.transport.state
        leader = state.acceptors[state.bullet]
        leader.log.append(omega_data)
        
        # Replicate to quorum
        return BulletActions.log_replication(state)
    
    def get_committed_log(self) -> List[Dict]:
        """Get committed log entries (replicated to quorum)"""
        if self.transport.state is None:
            return []
        return self.transport.state.acceptors[self.node_id].log.copy()
    
    def request_leadership(self) -> bool:
        """Request to become leader (for failover)"""
        state = self.transport.state
        if state is None:
            return False
        
        # Promote to candidate
        if not BulletActions.promote_candidate(state, self.node_id):
            return False
        
        # Request votes from quorum (send 1a)
        msg = BulletMessage(
            msg_type=MsgType.MSG_1A,
            sender=self.node_id,
            term=state.term + 1
        )
        self.transport.broadcast_to_quorum(msg)
        
        # Wait briefly for votes (simplified)
        time.sleep(0.5)
        
        # Try to elect self
        return BulletActions.leader_election(state, self.node_id)
    
    def transfer_leadership(self, new_leader: int) -> bool:
        """Transfer leadership to another node (magic bullet pass)"""
        if not self.is_leader():
            return False
        return BulletActions.magic_bullet_pass(self.transport.state, new_leader)
    
    def check_safety(self) -> Tuple[bool, str]:
        """Verify safety invariants"""
        return BulletInvariants.check_safety(self.transport.state)
    
    def status(self) -> Dict:
        """Get node status"""
        state = self.transport.state
        if state is None:
            return {"error": "not initialized"}
        
        acc = state.acceptors[self.node_id]
        safe, msg = self.check_safety()
        
        return {
            "node_id": self.node_id,
            "role": Role(acc.role).name,
            "term": state.term,
            "bullet": state.bullet,
            "is_leader": self.is_leader(),
            "log_len": len(acc.log),
            "quorum": list(state.quorum),
            "safety": {"ok": safe, "msg": msg},
            "peers": len(self.transport.peers),
            "msgs": len(state.msgs)
        }


# =============================================================================
# CLI (mirrors bullet.c interface)
# =============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bullet Consensus Protocol")
    parser.add_argument("--node", type=int, default=0, help="Node ID")
    parser.add_argument("--nodes", type=int, default=3, help="Total nodes")
    parser.add_argument("--port", type=int, default=9876, help="Listen port")
    parser.add_argument("--peers", type=str, default="", help="Peers: id:host:port,...")
    parser.add_argument("cmd", nargs="?", default="status", 
                       choices=["status", "start", "propose", "leader", "pass", "safety"])
    parser.add_argument("--value", type=str, default="{}", help="Value to propose (JSON)")
    parser.add_argument("--target", type=int, default=1, help="Target node for pass")
    args = parser.parse_args()
    
    bridge = BulletRingBridge(args.node, args.nodes)
    
    # Configure peers
    if args.peers:
        peers = []
        for p in args.peers.split(","):
            parts = p.split(":")
            peers.append((int(parts[0]), parts[1], int(parts[2])))
        bridge.configure_cluster(peers)
    
    if args.cmd == "start":
        if bridge.start(args.port):
            print(json.dumps(bridge.status(), indent=2))
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                bridge.transport.stop()
        
    elif args.cmd == "propose":
        value = json.loads(args.value)
        result = bridge.propose_omega(value)
        print(f"Propose: {'OK' if result else 'FAIL'}")
        
    elif args.cmd == "leader":
        result = bridge.request_leadership()
        print(f"Leadership: {'OK' if result else 'FAIL'}")
        
    elif args.cmd == "pass":
        result = bridge.transfer_leadership(args.target)
        print(f"Pass to {args.target}: {'OK' if result else 'FAIL'}")
        
    elif args.cmd == "safety":
        ok, msg = bridge.check_safety()
        print(f"Safety: {msg}")
        
    else:  # status
        print(json.dumps(bridge.status(), indent=2))


if __name__ == "__main__":
    main()
