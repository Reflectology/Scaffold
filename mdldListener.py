# Generated from mdld.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .mdldParser import mdldParser
else:
    from mdldParser import mdldParser

# This class defines a complete listener for a parse tree produced by mdldParser.
class mdldListener(ParseTreeListener):

    # Enter a parse tree produced by mdldParser#document.
    def enterDocument(self, ctx:mdldParser.DocumentContext):
        pass

    # Exit a parse tree produced by mdldParser#document.
    def exitDocument(self, ctx:mdldParser.DocumentContext):
        pass


    # Enter a parse tree produced by mdldParser#statementList.
    def enterStatementList(self, ctx:mdldParser.StatementListContext):
        pass

    # Exit a parse tree produced by mdldParser#statementList.
    def exitStatementList(self, ctx:mdldParser.StatementListContext):
        pass


    # Enter a parse tree produced by mdldParser#sep.
    def enterSep(self, ctx:mdldParser.SepContext):
        pass

    # Exit a parse tree produced by mdldParser#sep.
    def exitSep(self, ctx:mdldParser.SepContext):
        pass


    # Enter a parse tree produced by mdldParser#statement.
    def enterStatement(self, ctx:mdldParser.StatementContext):
        pass

    # Exit a parse tree produced by mdldParser#statement.
    def exitStatement(self, ctx:mdldParser.StatementContext):
        pass


    # Enter a parse tree produced by mdldParser#configSpaceDecl.
    def enterConfigSpaceDecl(self, ctx:mdldParser.ConfigSpaceDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#configSpaceDecl.
    def exitConfigSpaceDecl(self, ctx:mdldParser.ConfigSpaceDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#configSpaceExpr.
    def enterConfigSpaceExpr(self, ctx:mdldParser.ConfigSpaceExprContext):
        pass

    # Exit a parse tree produced by mdldParser#configSpaceExpr.
    def exitConfigSpaceExpr(self, ctx:mdldParser.ConfigSpaceExprContext):
        pass


    # Enter a parse tree produced by mdldParser#omega0.
    def enterOmega0(self, ctx:mdldParser.Omega0Context):
        pass

    # Exit a parse tree produced by mdldParser#omega0.
    def exitOmega0(self, ctx:mdldParser.Omega0Context):
        pass


    # Enter a parse tree produced by mdldParser#omegaN.
    def enterOmegaN(self, ctx:mdldParser.OmegaNContext):
        pass

    # Exit a parse tree produced by mdldParser#omegaN.
    def exitOmegaN(self, ctx:mdldParser.OmegaNContext):
        pass


    # Enter a parse tree produced by mdldParser#omegaFull.
    def enterOmegaFull(self, ctx:mdldParser.OmegaFullContext):
        pass

    # Exit a parse tree produced by mdldParser#omegaFull.
    def exitOmegaFull(self, ctx:mdldParser.OmegaFullContext):
        pass


    # Enter a parse tree produced by mdldParser#omegaList.
    def enterOmegaList(self, ctx:mdldParser.OmegaListContext):
        pass

    # Exit a parse tree produced by mdldParser#omegaList.
    def exitOmegaList(self, ctx:mdldParser.OmegaListContext):
        pass


    # Enter a parse tree produced by mdldParser#transformExpr.
    def enterTransformExpr(self, ctx:mdldParser.TransformExprContext):
        pass

    # Exit a parse tree produced by mdldParser#transformExpr.
    def exitTransformExpr(self, ctx:mdldParser.TransformExprContext):
        pass


    # Enter a parse tree produced by mdldParser#axiomStmt.
    def enterAxiomStmt(self, ctx:mdldParser.AxiomStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#axiomStmt.
    def exitAxiomStmt(self, ctx:mdldParser.AxiomStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#axiomKeyword.
    def enterAxiomKeyword(self, ctx:mdldParser.AxiomKeywordContext):
        pass

    # Exit a parse tree produced by mdldParser#axiomKeyword.
    def exitAxiomKeyword(self, ctx:mdldParser.AxiomKeywordContext):
        pass


    # Enter a parse tree produced by mdldParser#reflectologyStmt.
    def enterReflectologyStmt(self, ctx:mdldParser.ReflectologyStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#reflectologyStmt.
    def exitReflectologyStmt(self, ctx:mdldParser.ReflectologyStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#defineStmt.
    def enterDefineStmt(self, ctx:mdldParser.DefineStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#defineStmt.
    def exitDefineStmt(self, ctx:mdldParser.DefineStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#reduceStmt.
    def enterReduceStmt(self, ctx:mdldParser.ReduceStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#reduceStmt.
    def exitReduceStmt(self, ctx:mdldParser.ReduceStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#computeStmt.
    def enterComputeStmt(self, ctx:mdldParser.ComputeStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#computeStmt.
    def exitComputeStmt(self, ctx:mdldParser.ComputeStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#evaluateStmt.
    def enterEvaluateStmt(self, ctx:mdldParser.EvaluateStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#evaluateStmt.
    def exitEvaluateStmt(self, ctx:mdldParser.EvaluateStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#optimizeStmt.
    def enterOptimizeStmt(self, ctx:mdldParser.OptimizeStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#optimizeStmt.
    def exitOptimizeStmt(self, ctx:mdldParser.OptimizeStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#ireStmt.
    def enterIreStmt(self, ctx:mdldParser.IreStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#ireStmt.
    def exitIreStmt(self, ctx:mdldParser.IreStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#dualSymmetryStmt.
    def enterDualSymmetryStmt(self, ctx:mdldParser.DualSymmetryStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#dualSymmetryStmt.
    def exitDualSymmetryStmt(self, ctx:mdldParser.DualSymmetryStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#thetaExpr.
    def enterThetaExpr(self, ctx:mdldParser.ThetaExprContext):
        pass

    # Exit a parse tree produced by mdldParser#thetaExpr.
    def exitThetaExpr(self, ctx:mdldParser.ThetaExprContext):
        pass


    # Enter a parse tree produced by mdldParser#quotientExpr.
    def enterQuotientExpr(self, ctx:mdldParser.QuotientExprContext):
        pass

    # Exit a parse tree produced by mdldParser#quotientExpr.
    def exitQuotientExpr(self, ctx:mdldParser.QuotientExprContext):
        pass


    # Enter a parse tree produced by mdldParser#equivRel.
    def enterEquivRel(self, ctx:mdldParser.EquivRelContext):
        pass

    # Exit a parse tree produced by mdldParser#equivRel.
    def exitEquivRel(self, ctx:mdldParser.EquivRelContext):
        pass


    # Enter a parse tree produced by mdldParser#orbitExpr.
    def enterOrbitExpr(self, ctx:mdldParser.OrbitExprContext):
        pass

    # Exit a parse tree produced by mdldParser#orbitExpr.
    def exitOrbitExpr(self, ctx:mdldParser.OrbitExprContext):
        pass


    # Enter a parse tree produced by mdldParser#groupExpr.
    def enterGroupExpr(self, ctx:mdldParser.GroupExprContext):
        pass

    # Exit a parse tree produced by mdldParser#groupExpr.
    def exitGroupExpr(self, ctx:mdldParser.GroupExprContext):
        pass


    # Enter a parse tree produced by mdldParser#simplifyExpr.
    def enterSimplifyExpr(self, ctx:mdldParser.SimplifyExprContext):
        pass

    # Exit a parse tree produced by mdldParser#simplifyExpr.
    def exitSimplifyExpr(self, ctx:mdldParser.SimplifyExprContext):
        pass


    # Enter a parse tree produced by mdldParser#composeExpr.
    def enterComposeExpr(self, ctx:mdldParser.ComposeExprContext):
        pass

    # Exit a parse tree produced by mdldParser#composeExpr.
    def exitComposeExpr(self, ctx:mdldParser.ComposeExprContext):
        pass


    # Enter a parse tree produced by mdldParser#lossExpr.
    def enterLossExpr(self, ctx:mdldParser.LossExprContext):
        pass

    # Exit a parse tree produced by mdldParser#lossExpr.
    def exitLossExpr(self, ctx:mdldParser.LossExprContext):
        pass


    # Enter a parse tree produced by mdldParser#convergeExpr.
    def enterConvergeExpr(self, ctx:mdldParser.ConvergeExprContext):
        pass

    # Exit a parse tree produced by mdldParser#convergeExpr.
    def exitConvergeExpr(self, ctx:mdldParser.ConvergeExprContext):
        pass


    # Enter a parse tree produced by mdldParser#limitTarget.
    def enterLimitTarget(self, ctx:mdldParser.LimitTargetContext):
        pass

    # Exit a parse tree produced by mdldParser#limitTarget.
    def exitLimitTarget(self, ctx:mdldParser.LimitTargetContext):
        pass


    # Enter a parse tree produced by mdldParser#entropyExpr.
    def enterEntropyExpr(self, ctx:mdldParser.EntropyExprContext):
        pass

    # Exit a parse tree produced by mdldParser#entropyExpr.
    def exitEntropyExpr(self, ctx:mdldParser.EntropyExprContext):
        pass


    # Enter a parse tree produced by mdldParser#nonlinearExpr.
    def enterNonlinearExpr(self, ctx:mdldParser.NonlinearExprContext):
        pass

    # Exit a parse tree produced by mdldParser#nonlinearExpr.
    def exitNonlinearExpr(self, ctx:mdldParser.NonlinearExprContext):
        pass


    # Enter a parse tree produced by mdldParser#hyperrealExpr.
    def enterHyperrealExpr(self, ctx:mdldParser.HyperrealExprContext):
        pass

    # Exit a parse tree produced by mdldParser#hyperrealExpr.
    def exitHyperrealExpr(self, ctx:mdldParser.HyperrealExprContext):
        pass


    # Enter a parse tree produced by mdldParser#dimensionExpr.
    def enterDimensionExpr(self, ctx:mdldParser.DimensionExprContext):
        pass

    # Exit a parse tree produced by mdldParser#dimensionExpr.
    def exitDimensionExpr(self, ctx:mdldParser.DimensionExprContext):
        pass


    # Enter a parse tree produced by mdldParser#goodnessExpr.
    def enterGoodnessExpr(self, ctx:mdldParser.GoodnessExprContext):
        pass

    # Exit a parse tree produced by mdldParser#goodnessExpr.
    def exitGoodnessExpr(self, ctx:mdldParser.GoodnessExprContext):
        pass


    # Enter a parse tree produced by mdldParser#costExpr.
    def enterCostExpr(self, ctx:mdldParser.CostExprContext):
        pass

    # Exit a parse tree produced by mdldParser#costExpr.
    def exitCostExpr(self, ctx:mdldParser.CostExprContext):
        pass


    # Enter a parse tree produced by mdldParser#preserveExpr.
    def enterPreserveExpr(self, ctx:mdldParser.PreserveExprContext):
        pass

    # Exit a parse tree produced by mdldParser#preserveExpr.
    def exitPreserveExpr(self, ctx:mdldParser.PreserveExprContext):
        pass


    # Enter a parse tree produced by mdldParser#energyExpr.
    def enterEnergyExpr(self, ctx:mdldParser.EnergyExprContext):
        pass

    # Exit a parse tree produced by mdldParser#energyExpr.
    def exitEnergyExpr(self, ctx:mdldParser.EnergyExprContext):
        pass


    # Enter a parse tree produced by mdldParser#divergeExpr.
    def enterDivergeExpr(self, ctx:mdldParser.DivergeExprContext):
        pass

    # Exit a parse tree produced by mdldParser#divergeExpr.
    def exitDivergeExpr(self, ctx:mdldParser.DivergeExprContext):
        pass


    # Enter a parse tree produced by mdldParser#gradientExpr.
    def enterGradientExpr(self, ctx:mdldParser.GradientExprContext):
        pass

    # Exit a parse tree produced by mdldParser#gradientExpr.
    def exitGradientExpr(self, ctx:mdldParser.GradientExprContext):
        pass


    # Enter a parse tree produced by mdldParser#dynamicsExpr.
    def enterDynamicsExpr(self, ctx:mdldParser.DynamicsExprContext):
        pass

    # Exit a parse tree produced by mdldParser#dynamicsExpr.
    def exitDynamicsExpr(self, ctx:mdldParser.DynamicsExprContext):
        pass


    # Enter a parse tree produced by mdldParser#probExpr.
    def enterProbExpr(self, ctx:mdldParser.ProbExprContext):
        pass

    # Exit a parse tree produced by mdldParser#probExpr.
    def exitProbExpr(self, ctx:mdldParser.ProbExprContext):
        pass


    # Enter a parse tree produced by mdldParser#stepExpr.
    def enterStepExpr(self, ctx:mdldParser.StepExprContext):
        pass

    # Exit a parse tree produced by mdldParser#stepExpr.
    def exitStepExpr(self, ctx:mdldParser.StepExprContext):
        pass


    # Enter a parse tree produced by mdldParser#stabilizeExpr.
    def enterStabilizeExpr(self, ctx:mdldParser.StabilizeExprContext):
        pass

    # Exit a parse tree produced by mdldParser#stabilizeExpr.
    def exitStabilizeExpr(self, ctx:mdldParser.StabilizeExprContext):
        pass


    # Enter a parse tree produced by mdldParser#transformOp.
    def enterTransformOp(self, ctx:mdldParser.TransformOpContext):
        pass

    # Exit a parse tree produced by mdldParser#transformOp.
    def exitTransformOp(self, ctx:mdldParser.TransformOpContext):
        pass


    # Enter a parse tree produced by mdldParser#pathExpr.
    def enterPathExpr(self, ctx:mdldParser.PathExprContext):
        pass

    # Exit a parse tree produced by mdldParser#pathExpr.
    def exitPathExpr(self, ctx:mdldParser.PathExprContext):
        pass


    # Enter a parse tree produced by mdldParser#fluxExpr.
    def enterFluxExpr(self, ctx:mdldParser.FluxExprContext):
        pass

    # Exit a parse tree produced by mdldParser#fluxExpr.
    def exitFluxExpr(self, ctx:mdldParser.FluxExprContext):
        pass


    # Enter a parse tree produced by mdldParser#causalExpr.
    def enterCausalExpr(self, ctx:mdldParser.CausalExprContext):
        pass

    # Exit a parse tree produced by mdldParser#causalExpr.
    def exitCausalExpr(self, ctx:mdldParser.CausalExprContext):
        pass


    # Enter a parse tree produced by mdldParser#optimizeExpr.
    def enterOptimizeExpr(self, ctx:mdldParser.OptimizeExprContext):
        pass

    # Exit a parse tree produced by mdldParser#optimizeExpr.
    def exitOptimizeExpr(self, ctx:mdldParser.OptimizeExprContext):
        pass


    # Enter a parse tree produced by mdldParser#lineageExpr.
    def enterLineageExpr(self, ctx:mdldParser.LineageExprContext):
        pass

    # Exit a parse tree produced by mdldParser#lineageExpr.
    def exitLineageExpr(self, ctx:mdldParser.LineageExprContext):
        pass


    # Enter a parse tree produced by mdldParser#emergeExpr.
    def enterEmergeExpr(self, ctx:mdldParser.EmergeExprContext):
        pass

    # Exit a parse tree produced by mdldParser#emergeExpr.
    def exitEmergeExpr(self, ctx:mdldParser.EmergeExprContext):
        pass


    # Enter a parse tree produced by mdldParser#dualExpr.
    def enterDualExpr(self, ctx:mdldParser.DualExprContext):
        pass

    # Exit a parse tree produced by mdldParser#dualExpr.
    def exitDualExpr(self, ctx:mdldParser.DualExprContext):
        pass


    # Enter a parse tree produced by mdldParser#nlpStmt.
    def enterNlpStmt(self, ctx:mdldParser.NlpStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#nlpStmt.
    def exitNlpStmt(self, ctx:mdldParser.NlpStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#patternMatchStmt.
    def enterPatternMatchStmt(self, ctx:mdldParser.PatternMatchStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#patternMatchStmt.
    def exitPatternMatchStmt(self, ctx:mdldParser.PatternMatchStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#nlpProcessStmt.
    def enterNlpProcessStmt(self, ctx:mdldParser.NlpProcessStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#nlpProcessStmt.
    def exitNlpProcessStmt(self, ctx:mdldParser.NlpProcessStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#nlpTransformStmt.
    def enterNlpTransformStmt(self, ctx:mdldParser.NlpTransformStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#nlpTransformStmt.
    def exitNlpTransformStmt(self, ctx:mdldParser.NlpTransformStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#regexStmt.
    def enterRegexStmt(self, ctx:mdldParser.RegexStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#regexStmt.
    def exitRegexStmt(self, ctx:mdldParser.RegexStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#regexMatchStmt.
    def enterRegexMatchStmt(self, ctx:mdldParser.RegexMatchStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#regexMatchStmt.
    def exitRegexMatchStmt(self, ctx:mdldParser.RegexMatchStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#regexReplaceStmt.
    def enterRegexReplaceStmt(self, ctx:mdldParser.RegexReplaceStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#regexReplaceStmt.
    def exitRegexReplaceStmt(self, ctx:mdldParser.RegexReplaceStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#regexExtractStmt.
    def enterRegexExtractStmt(self, ctx:mdldParser.RegexExtractStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#regexExtractStmt.
    def exitRegexExtractStmt(self, ctx:mdldParser.RegexExtractStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#regexSplitStmt.
    def enterRegexSplitStmt(self, ctx:mdldParser.RegexSplitStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#regexSplitStmt.
    def exitRegexSplitStmt(self, ctx:mdldParser.RegexSplitStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#abiDecl.
    def enterAbiDecl(self, ctx:mdldParser.AbiDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#abiDecl.
    def exitAbiDecl(self, ctx:mdldParser.AbiDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#abiBody.
    def enterAbiBody(self, ctx:mdldParser.AbiBodyContext):
        pass

    # Exit a parse tree produced by mdldParser#abiBody.
    def exitAbiBody(self, ctx:mdldParser.AbiBodyContext):
        pass


    # Enter a parse tree produced by mdldParser#abiMember.
    def enterAbiMember(self, ctx:mdldParser.AbiMemberContext):
        pass

    # Exit a parse tree produced by mdldParser#abiMember.
    def exitAbiMember(self, ctx:mdldParser.AbiMemberContext):
        pass


    # Enter a parse tree produced by mdldParser#apiDecl.
    def enterApiDecl(self, ctx:mdldParser.ApiDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#apiDecl.
    def exitApiDecl(self, ctx:mdldParser.ApiDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#apiBody.
    def enterApiBody(self, ctx:mdldParser.ApiBodyContext):
        pass

    # Exit a parse tree produced by mdldParser#apiBody.
    def exitApiBody(self, ctx:mdldParser.ApiBodyContext):
        pass


    # Enter a parse tree produced by mdldParser#apiEndpoint.
    def enterApiEndpoint(self, ctx:mdldParser.ApiEndpointContext):
        pass

    # Exit a parse tree produced by mdldParser#apiEndpoint.
    def exitApiEndpoint(self, ctx:mdldParser.ApiEndpointContext):
        pass


    # Enter a parse tree produced by mdldParser#httpMethod.
    def enterHttpMethod(self, ctx:mdldParser.HttpMethodContext):
        pass

    # Exit a parse tree produced by mdldParser#httpMethod.
    def exitHttpMethod(self, ctx:mdldParser.HttpMethodContext):
        pass


    # Enter a parse tree produced by mdldParser#ffiCall.
    def enterFfiCall(self, ctx:mdldParser.FfiCallContext):
        pass

    # Exit a parse tree produced by mdldParser#ffiCall.
    def exitFfiCall(self, ctx:mdldParser.FfiCallContext):
        pass


    # Enter a parse tree produced by mdldParser#exportStmt.
    def enterExportStmt(self, ctx:mdldParser.ExportStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#exportStmt.
    def exitExportStmt(self, ctx:mdldParser.ExportStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#importStmt.
    def enterImportStmt(self, ctx:mdldParser.ImportStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#importStmt.
    def exitImportStmt(self, ctx:mdldParser.ImportStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#matrixStmt.
    def enterMatrixStmt(self, ctx:mdldParser.MatrixStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#matrixStmt.
    def exitMatrixStmt(self, ctx:mdldParser.MatrixStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#matrixLiteral.
    def enterMatrixLiteral(self, ctx:mdldParser.MatrixLiteralContext):
        pass

    # Exit a parse tree produced by mdldParser#matrixLiteral.
    def exitMatrixLiteral(self, ctx:mdldParser.MatrixLiteralContext):
        pass


    # Enter a parse tree produced by mdldParser#matrixRows.
    def enterMatrixRows(self, ctx:mdldParser.MatrixRowsContext):
        pass

    # Exit a parse tree produced by mdldParser#matrixRows.
    def exitMatrixRows(self, ctx:mdldParser.MatrixRowsContext):
        pass


    # Enter a parse tree produced by mdldParser#matrixRow.
    def enterMatrixRow(self, ctx:mdldParser.MatrixRowContext):
        pass

    # Exit a parse tree produced by mdldParser#matrixRow.
    def exitMatrixRow(self, ctx:mdldParser.MatrixRowContext):
        pass


    # Enter a parse tree produced by mdldParser#matrixOperation.
    def enterMatrixOperation(self, ctx:mdldParser.MatrixOperationContext):
        pass

    # Exit a parse tree produced by mdldParser#matrixOperation.
    def exitMatrixOperation(self, ctx:mdldParser.MatrixOperationContext):
        pass


    # Enter a parse tree produced by mdldParser#matrixMul.
    def enterMatrixMul(self, ctx:mdldParser.MatrixMulContext):
        pass

    # Exit a parse tree produced by mdldParser#matrixMul.
    def exitMatrixMul(self, ctx:mdldParser.MatrixMulContext):
        pass


    # Enter a parse tree produced by mdldParser#matrixAccess.
    def enterMatrixAccess(self, ctx:mdldParser.MatrixAccessContext):
        pass

    # Exit a parse tree produced by mdldParser#matrixAccess.
    def exitMatrixAccess(self, ctx:mdldParser.MatrixAccessContext):
        pass


    # Enter a parse tree produced by mdldParser#typeDecl.
    def enterTypeDecl(self, ctx:mdldParser.TypeDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#typeDecl.
    def exitTypeDecl(self, ctx:mdldParser.TypeDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#typeParamsOpt.
    def enterTypeParamsOpt(self, ctx:mdldParser.TypeParamsOptContext):
        pass

    # Exit a parse tree produced by mdldParser#typeParamsOpt.
    def exitTypeParamsOpt(self, ctx:mdldParser.TypeParamsOptContext):
        pass


    # Enter a parse tree produced by mdldParser#typeParamList.
    def enterTypeParamList(self, ctx:mdldParser.TypeParamListContext):
        pass

    # Exit a parse tree produced by mdldParser#typeParamList.
    def exitTypeParamList(self, ctx:mdldParser.TypeParamListContext):
        pass


    # Enter a parse tree produced by mdldParser#typeVar.
    def enterTypeVar(self, ctx:mdldParser.TypeVarContext):
        pass

    # Exit a parse tree produced by mdldParser#typeVar.
    def exitTypeVar(self, ctx:mdldParser.TypeVarContext):
        pass


    # Enter a parse tree produced by mdldParser#typeExpr.
    def enterTypeExpr(self, ctx:mdldParser.TypeExprContext):
        pass

    # Exit a parse tree produced by mdldParser#typeExpr.
    def exitTypeExpr(self, ctx:mdldParser.TypeExprContext):
        pass


    # Enter a parse tree produced by mdldParser#typeArgsOpt.
    def enterTypeArgsOpt(self, ctx:mdldParser.TypeArgsOptContext):
        pass

    # Exit a parse tree produced by mdldParser#typeArgsOpt.
    def exitTypeArgsOpt(self, ctx:mdldParser.TypeArgsOptContext):
        pass


    # Enter a parse tree produced by mdldParser#variantDecl.
    def enterVariantDecl(self, ctx:mdldParser.VariantDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#variantDecl.
    def exitVariantDecl(self, ctx:mdldParser.VariantDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#variantBody.
    def enterVariantBody(self, ctx:mdldParser.VariantBodyContext):
        pass

    # Exit a parse tree produced by mdldParser#variantBody.
    def exitVariantBody(self, ctx:mdldParser.VariantBodyContext):
        pass


    # Enter a parse tree produced by mdldParser#variantCase.
    def enterVariantCase(self, ctx:mdldParser.VariantCaseContext):
        pass

    # Exit a parse tree produced by mdldParser#variantCase.
    def exitVariantCase(self, ctx:mdldParser.VariantCaseContext):
        pass


    # Enter a parse tree produced by mdldParser#moduleDecl.
    def enterModuleDecl(self, ctx:mdldParser.ModuleDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#moduleDecl.
    def exitModuleDecl(self, ctx:mdldParser.ModuleDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#moduleExpr.
    def enterModuleExpr(self, ctx:mdldParser.ModuleExprContext):
        pass

    # Exit a parse tree produced by mdldParser#moduleExpr.
    def exitModuleExpr(self, ctx:mdldParser.ModuleExprContext):
        pass


    # Enter a parse tree produced by mdldParser#moduleType.
    def enterModuleType(self, ctx:mdldParser.ModuleTypeContext):
        pass

    # Exit a parse tree produced by mdldParser#moduleType.
    def exitModuleType(self, ctx:mdldParser.ModuleTypeContext):
        pass


    # Enter a parse tree produced by mdldParser#sigItemList.
    def enterSigItemList(self, ctx:mdldParser.SigItemListContext):
        pass

    # Exit a parse tree produced by mdldParser#sigItemList.
    def exitSigItemList(self, ctx:mdldParser.SigItemListContext):
        pass


    # Enter a parse tree produced by mdldParser#sigItem.
    def enterSigItem(self, ctx:mdldParser.SigItemContext):
        pass

    # Exit a parse tree produced by mdldParser#sigItem.
    def exitSigItem(self, ctx:mdldParser.SigItemContext):
        pass


    # Enter a parse tree produced by mdldParser#functorApp.
    def enterFunctorApp(self, ctx:mdldParser.FunctorAppContext):
        pass

    # Exit a parse tree produced by mdldParser#functorApp.
    def exitFunctorApp(self, ctx:mdldParser.FunctorAppContext):
        pass


    # Enter a parse tree produced by mdldParser#openStmt.
    def enterOpenStmt(self, ctx:mdldParser.OpenStmtContext):
        pass

    # Exit a parse tree produced by mdldParser#openStmt.
    def exitOpenStmt(self, ctx:mdldParser.OpenStmtContext):
        pass


    # Enter a parse tree produced by mdldParser#typeList.
    def enterTypeList(self, ctx:mdldParser.TypeListContext):
        pass

    # Exit a parse tree produced by mdldParser#typeList.
    def exitTypeList(self, ctx:mdldParser.TypeListContext):
        pass


    # Enter a parse tree produced by mdldParser#recordDecl.
    def enterRecordDecl(self, ctx:mdldParser.RecordDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#recordDecl.
    def exitRecordDecl(self, ctx:mdldParser.RecordDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#fieldDeclList.
    def enterFieldDeclList(self, ctx:mdldParser.FieldDeclListContext):
        pass

    # Exit a parse tree produced by mdldParser#fieldDeclList.
    def exitFieldDeclList(self, ctx:mdldParser.FieldDeclListContext):
        pass


    # Enter a parse tree produced by mdldParser#fieldDecl.
    def enterFieldDecl(self, ctx:mdldParser.FieldDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#fieldDecl.
    def exitFieldDecl(self, ctx:mdldParser.FieldDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#funcDecl.
    def enterFuncDecl(self, ctx:mdldParser.FuncDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#funcDecl.
    def exitFuncDecl(self, ctx:mdldParser.FuncDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#paramListOpt.
    def enterParamListOpt(self, ctx:mdldParser.ParamListOptContext):
        pass

    # Exit a parse tree produced by mdldParser#paramListOpt.
    def exitParamListOpt(self, ctx:mdldParser.ParamListOptContext):
        pass


    # Enter a parse tree produced by mdldParser#paramList.
    def enterParamList(self, ctx:mdldParser.ParamListContext):
        pass

    # Exit a parse tree produced by mdldParser#paramList.
    def exitParamList(self, ctx:mdldParser.ParamListContext):
        pass


    # Enter a parse tree produced by mdldParser#param.
    def enterParam(self, ctx:mdldParser.ParamContext):
        pass

    # Exit a parse tree produced by mdldParser#param.
    def exitParam(self, ctx:mdldParser.ParamContext):
        pass


    # Enter a parse tree produced by mdldParser#ioDecl.
    def enterIoDecl(self, ctx:mdldParser.IoDeclContext):
        pass

    # Exit a parse tree produced by mdldParser#ioDecl.
    def exitIoDecl(self, ctx:mdldParser.IoDeclContext):
        pass


    # Enter a parse tree produced by mdldParser#ioExpr.
    def enterIoExpr(self, ctx:mdldParser.IoExprContext):
        pass

    # Exit a parse tree produced by mdldParser#ioExpr.
    def exitIoExpr(self, ctx:mdldParser.IoExprContext):
        pass


    # Enter a parse tree produced by mdldParser#doBlock.
    def enterDoBlock(self, ctx:mdldParser.DoBlockContext):
        pass

    # Exit a parse tree produced by mdldParser#doBlock.
    def exitDoBlock(self, ctx:mdldParser.DoBlockContext):
        pass


    # Enter a parse tree produced by mdldParser#ioStatementList.
    def enterIoStatementList(self, ctx:mdldParser.IoStatementListContext):
        pass

    # Exit a parse tree produced by mdldParser#ioStatementList.
    def exitIoStatementList(self, ctx:mdldParser.IoStatementListContext):
        pass


    # Enter a parse tree produced by mdldParser#ioStatement.
    def enterIoStatement(self, ctx:mdldParser.IoStatementContext):
        pass

    # Exit a parse tree produced by mdldParser#ioStatement.
    def exitIoStatement(self, ctx:mdldParser.IoStatementContext):
        pass


    # Enter a parse tree produced by mdldParser#assignment.
    def enterAssignment(self, ctx:mdldParser.AssignmentContext):
        pass

    # Exit a parse tree produced by mdldParser#assignment.
    def exitAssignment(self, ctx:mdldParser.AssignmentContext):
        pass


    # Enter a parse tree produced by mdldParser#equation.
    def enterEquation(self, ctx:mdldParser.EquationContext):
        pass

    # Exit a parse tree produced by mdldParser#equation.
    def exitEquation(self, ctx:mdldParser.EquationContext):
        pass


    # Enter a parse tree produced by mdldParser#inequality.
    def enterInequality(self, ctx:mdldParser.InequalityContext):
        pass

    # Exit a parse tree produced by mdldParser#inequality.
    def exitInequality(self, ctx:mdldParser.InequalityContext):
        pass


    # Enter a parse tree produced by mdldParser#implication.
    def enterImplication(self, ctx:mdldParser.ImplicationContext):
        pass

    # Exit a parse tree produced by mdldParser#implication.
    def exitImplication(self, ctx:mdldParser.ImplicationContext):
        pass


    # Enter a parse tree produced by mdldParser#quantified.
    def enterQuantified(self, ctx:mdldParser.QuantifiedContext):
        pass

    # Exit a parse tree produced by mdldParser#quantified.
    def exitQuantified(self, ctx:mdldParser.QuantifiedContext):
        pass


    # Enter a parse tree produced by mdldParser#quantifier.
    def enterQuantifier(self, ctx:mdldParser.QuantifierContext):
        pass

    # Exit a parse tree produced by mdldParser#quantifier.
    def exitQuantifier(self, ctx:mdldParser.QuantifierContext):
        pass


    # Enter a parse tree produced by mdldParser#binderList.
    def enterBinderList(self, ctx:mdldParser.BinderListContext):
        pass

    # Exit a parse tree produced by mdldParser#binderList.
    def exitBinderList(self, ctx:mdldParser.BinderListContext):
        pass


    # Enter a parse tree produced by mdldParser#binder.
    def enterBinder(self, ctx:mdldParser.BinderContext):
        pass

    # Exit a parse tree produced by mdldParser#binder.
    def exitBinder(self, ctx:mdldParser.BinderContext):
        pass


    # Enter a parse tree produced by mdldParser#probability.
    def enterProbability(self, ctx:mdldParser.ProbabilityContext):
        pass

    # Exit a parse tree produced by mdldParser#probability.
    def exitProbability(self, ctx:mdldParser.ProbabilityContext):
        pass


    # Enter a parse tree produced by mdldParser#formula.
    def enterFormula(self, ctx:mdldParser.FormulaContext):
        pass

    # Exit a parse tree produced by mdldParser#formula.
    def exitFormula(self, ctx:mdldParser.FormulaContext):
        pass


    # Enter a parse tree produced by mdldParser#disjunction.
    def enterDisjunction(self, ctx:mdldParser.DisjunctionContext):
        pass

    # Exit a parse tree produced by mdldParser#disjunction.
    def exitDisjunction(self, ctx:mdldParser.DisjunctionContext):
        pass


    # Enter a parse tree produced by mdldParser#conjunction.
    def enterConjunction(self, ctx:mdldParser.ConjunctionContext):
        pass

    # Exit a parse tree produced by mdldParser#conjunction.
    def exitConjunction(self, ctx:mdldParser.ConjunctionContext):
        pass


    # Enter a parse tree produced by mdldParser#negation.
    def enterNegation(self, ctx:mdldParser.NegationContext):
        pass

    # Exit a parse tree produced by mdldParser#negation.
    def exitNegation(self, ctx:mdldParser.NegationContext):
        pass


    # Enter a parse tree produced by mdldParser#atom.
    def enterAtom(self, ctx:mdldParser.AtomContext):
        pass

    # Exit a parse tree produced by mdldParser#atom.
    def exitAtom(self, ctx:mdldParser.AtomContext):
        pass


    # Enter a parse tree produced by mdldParser#relation.
    def enterRelation(self, ctx:mdldParser.RelationContext):
        pass

    # Exit a parse tree produced by mdldParser#relation.
    def exitRelation(self, ctx:mdldParser.RelationContext):
        pass


    # Enter a parse tree produced by mdldParser#predicate.
    def enterPredicate(self, ctx:mdldParser.PredicateContext):
        pass

    # Exit a parse tree produced by mdldParser#predicate.
    def exitPredicate(self, ctx:mdldParser.PredicateContext):
        pass


    # Enter a parse tree produced by mdldParser#argList.
    def enterArgList(self, ctx:mdldParser.ArgListContext):
        pass

    # Exit a parse tree produced by mdldParser#argList.
    def exitArgList(self, ctx:mdldParser.ArgListContext):
        pass


    # Enter a parse tree produced by mdldParser#expr.
    def enterExpr(self, ctx:mdldParser.ExprContext):
        pass

    # Exit a parse tree produced by mdldParser#expr.
    def exitExpr(self, ctx:mdldParser.ExprContext):
        pass


    # Enter a parse tree produced by mdldParser#term.
    def enterTerm(self, ctx:mdldParser.TermContext):
        pass

    # Exit a parse tree produced by mdldParser#term.
    def exitTerm(self, ctx:mdldParser.TermContext):
        pass


    # Enter a parse tree produced by mdldParser#factor.
    def enterFactor(self, ctx:mdldParser.FactorContext):
        pass

    # Exit a parse tree produced by mdldParser#factor.
    def exitFactor(self, ctx:mdldParser.FactorContext):
        pass


    # Enter a parse tree produced by mdldParser#postfix.
    def enterPostfix(self, ctx:mdldParser.PostfixContext):
        pass

    # Exit a parse tree produced by mdldParser#postfix.
    def exitPostfix(self, ctx:mdldParser.PostfixContext):
        pass


    # Enter a parse tree produced by mdldParser#postfixOp.
    def enterPostfixOp(self, ctx:mdldParser.PostfixOpContext):
        pass

    # Exit a parse tree produced by mdldParser#postfixOp.
    def exitPostfixOp(self, ctx:mdldParser.PostfixOpContext):
        pass


    # Enter a parse tree produced by mdldParser#subscript.
    def enterSubscript(self, ctx:mdldParser.SubscriptContext):
        pass

    # Exit a parse tree produced by mdldParser#subscript.
    def exitSubscript(self, ctx:mdldParser.SubscriptContext):
        pass


    # Enter a parse tree produced by mdldParser#primary.
    def enterPrimary(self, ctx:mdldParser.PrimaryContext):
        pass

    # Exit a parse tree produced by mdldParser#primary.
    def exitPrimary(self, ctx:mdldParser.PrimaryContext):
        pass


    # Enter a parse tree produced by mdldParser#letExpr.
    def enterLetExpr(self, ctx:mdldParser.LetExprContext):
        pass

    # Exit a parse tree produced by mdldParser#letExpr.
    def exitLetExpr(self, ctx:mdldParser.LetExprContext):
        pass


    # Enter a parse tree produced by mdldParser#letBinding.
    def enterLetBinding(self, ctx:mdldParser.LetBindingContext):
        pass

    # Exit a parse tree produced by mdldParser#letBinding.
    def exitLetBinding(self, ctx:mdldParser.LetBindingContext):
        pass


    # Enter a parse tree produced by mdldParser#letRecExpr.
    def enterLetRecExpr(self, ctx:mdldParser.LetRecExprContext):
        pass

    # Exit a parse tree produced by mdldParser#letRecExpr.
    def exitLetRecExpr(self, ctx:mdldParser.LetRecExprContext):
        pass


    # Enter a parse tree produced by mdldParser#recBindingList.
    def enterRecBindingList(self, ctx:mdldParser.RecBindingListContext):
        pass

    # Exit a parse tree produced by mdldParser#recBindingList.
    def exitRecBindingList(self, ctx:mdldParser.RecBindingListContext):
        pass


    # Enter a parse tree produced by mdldParser#recBinding.
    def enterRecBinding(self, ctx:mdldParser.RecBindingContext):
        pass

    # Exit a parse tree produced by mdldParser#recBinding.
    def exitRecBinding(self, ctx:mdldParser.RecBindingContext):
        pass


    # Enter a parse tree produced by mdldParser#ifExpr.
    def enterIfExpr(self, ctx:mdldParser.IfExprContext):
        pass

    # Exit a parse tree produced by mdldParser#ifExpr.
    def exitIfExpr(self, ctx:mdldParser.IfExprContext):
        pass


    # Enter a parse tree produced by mdldParser#elifChain.
    def enterElifChain(self, ctx:mdldParser.ElifChainContext):
        pass

    # Exit a parse tree produced by mdldParser#elifChain.
    def exitElifChain(self, ctx:mdldParser.ElifChainContext):
        pass


    # Enter a parse tree produced by mdldParser#elifClause.
    def enterElifClause(self, ctx:mdldParser.ElifClauseContext):
        pass

    # Exit a parse tree produced by mdldParser#elifClause.
    def exitElifClause(self, ctx:mdldParser.ElifClauseContext):
        pass


    # Enter a parse tree produced by mdldParser#matchExpr.
    def enterMatchExpr(self, ctx:mdldParser.MatchExprContext):
        pass

    # Exit a parse tree produced by mdldParser#matchExpr.
    def exitMatchExpr(self, ctx:mdldParser.MatchExprContext):
        pass


    # Enter a parse tree produced by mdldParser#matchCases.
    def enterMatchCases(self, ctx:mdldParser.MatchCasesContext):
        pass

    # Exit a parse tree produced by mdldParser#matchCases.
    def exitMatchCases(self, ctx:mdldParser.MatchCasesContext):
        pass


    # Enter a parse tree produced by mdldParser#matchCase.
    def enterMatchCase(self, ctx:mdldParser.MatchCaseContext):
        pass

    # Exit a parse tree produced by mdldParser#matchCase.
    def exitMatchCase(self, ctx:mdldParser.MatchCaseContext):
        pass


    # Enter a parse tree produced by mdldParser#guardOpt.
    def enterGuardOpt(self, ctx:mdldParser.GuardOptContext):
        pass

    # Exit a parse tree produced by mdldParser#guardOpt.
    def exitGuardOpt(self, ctx:mdldParser.GuardOptContext):
        pass


    # Enter a parse tree produced by mdldParser#pattern.
    def enterPattern(self, ctx:mdldParser.PatternContext):
        pass

    # Exit a parse tree produced by mdldParser#pattern.
    def exitPattern(self, ctx:mdldParser.PatternContext):
        pass


    # Enter a parse tree produced by mdldParser#patternAtom.
    def enterPatternAtom(self, ctx:mdldParser.PatternAtomContext):
        pass

    # Exit a parse tree produced by mdldParser#patternAtom.
    def exitPatternAtom(self, ctx:mdldParser.PatternAtomContext):
        pass


    # Enter a parse tree produced by mdldParser#patternSuffix.
    def enterPatternSuffix(self, ctx:mdldParser.PatternSuffixContext):
        pass

    # Exit a parse tree produced by mdldParser#patternSuffix.
    def exitPatternSuffix(self, ctx:mdldParser.PatternSuffixContext):
        pass


    # Enter a parse tree produced by mdldParser#patternList.
    def enterPatternList(self, ctx:mdldParser.PatternListContext):
        pass

    # Exit a parse tree produced by mdldParser#patternList.
    def exitPatternList(self, ctx:mdldParser.PatternListContext):
        pass


    # Enter a parse tree produced by mdldParser#fieldPatternList.
    def enterFieldPatternList(self, ctx:mdldParser.FieldPatternListContext):
        pass

    # Exit a parse tree produced by mdldParser#fieldPatternList.
    def exitFieldPatternList(self, ctx:mdldParser.FieldPatternListContext):
        pass


    # Enter a parse tree produced by mdldParser#fieldPattern.
    def enterFieldPattern(self, ctx:mdldParser.FieldPatternContext):
        pass

    # Exit a parse tree produced by mdldParser#fieldPattern.
    def exitFieldPattern(self, ctx:mdldParser.FieldPatternContext):
        pass


    # Enter a parse tree produced by mdldParser#tryExpr.
    def enterTryExpr(self, ctx:mdldParser.TryExprContext):
        pass

    # Exit a parse tree produced by mdldParser#tryExpr.
    def exitTryExpr(self, ctx:mdldParser.TryExprContext):
        pass


    # Enter a parse tree produced by mdldParser#raiseExpr.
    def enterRaiseExpr(self, ctx:mdldParser.RaiseExprContext):
        pass

    # Exit a parse tree produced by mdldParser#raiseExpr.
    def exitRaiseExpr(self, ctx:mdldParser.RaiseExprContext):
        pass


    # Enter a parse tree produced by mdldParser#setComprehension.
    def enterSetComprehension(self, ctx:mdldParser.SetComprehensionContext):
        pass

    # Exit a parse tree produced by mdldParser#setComprehension.
    def exitSetComprehension(self, ctx:mdldParser.SetComprehensionContext):
        pass


    # Enter a parse tree produced by mdldParser#tupleExpr.
    def enterTupleExpr(self, ctx:mdldParser.TupleExprContext):
        pass

    # Exit a parse tree produced by mdldParser#tupleExpr.
    def exitTupleExpr(self, ctx:mdldParser.TupleExprContext):
        pass


    # Enter a parse tree produced by mdldParser#exprList.
    def enterExprList(self, ctx:mdldParser.ExprListContext):
        pass

    # Exit a parse tree produced by mdldParser#exprList.
    def exitExprList(self, ctx:mdldParser.ExprListContext):
        pass


    # Enter a parse tree produced by mdldParser#lambdaExpr.
    def enterLambdaExpr(self, ctx:mdldParser.LambdaExprContext):
        pass

    # Exit a parse tree produced by mdldParser#lambdaExpr.
    def exitLambdaExpr(self, ctx:mdldParser.LambdaExprContext):
        pass


    # Enter a parse tree produced by mdldParser#recordExpr.
    def enterRecordExpr(self, ctx:mdldParser.RecordExprContext):
        pass

    # Exit a parse tree produced by mdldParser#recordExpr.
    def exitRecordExpr(self, ctx:mdldParser.RecordExprContext):
        pass


    # Enter a parse tree produced by mdldParser#fieldList.
    def enterFieldList(self, ctx:mdldParser.FieldListContext):
        pass

    # Exit a parse tree produced by mdldParser#fieldList.
    def exitFieldList(self, ctx:mdldParser.FieldListContext):
        pass


    # Enter a parse tree produced by mdldParser#field.
    def enterField(self, ctx:mdldParser.FieldContext):
        pass

    # Exit a parse tree produced by mdldParser#field.
    def exitField(self, ctx:mdldParser.FieldContext):
        pass


    # Enter a parse tree produced by mdldParser#funcCall.
    def enterFuncCall(self, ctx:mdldParser.FuncCallContext):
        pass

    # Exit a parse tree produced by mdldParser#funcCall.
    def exitFuncCall(self, ctx:mdldParser.FuncCallContext):
        pass


    # Enter a parse tree produced by mdldParser#lvalue.
    def enterLvalue(self, ctx:mdldParser.LvalueContext):
        pass

    # Exit a parse tree produced by mdldParser#lvalue.
    def exitLvalue(self, ctx:mdldParser.LvalueContext):
        pass


    # Enter a parse tree produced by mdldParser#lvalueSuffix.
    def enterLvalueSuffix(self, ctx:mdldParser.LvalueSuffixContext):
        pass

    # Exit a parse tree produced by mdldParser#lvalueSuffix.
    def exitLvalueSuffix(self, ctx:mdldParser.LvalueSuffixContext):
        pass


    # Enter a parse tree produced by mdldParser#comment.
    def enterComment(self, ctx:mdldParser.CommentContext):
        pass

    # Exit a parse tree produced by mdldParser#comment.
    def exitComment(self, ctx:mdldParser.CommentContext):
        pass



del mdldParser