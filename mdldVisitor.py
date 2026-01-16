# Generated from mdld.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .mdldParser import mdldParser
else:
    from mdldParser import mdldParser

# This class defines a complete generic visitor for a parse tree produced by mdldParser.

class mdldVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by mdldParser#document.
    def visitDocument(self, ctx:mdldParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#statementList.
    def visitStatementList(self, ctx:mdldParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#sep.
    def visitSep(self, ctx:mdldParser.SepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#statement.
    def visitStatement(self, ctx:mdldParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#configSpaceDecl.
    def visitConfigSpaceDecl(self, ctx:mdldParser.ConfigSpaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#configSpaceExpr.
    def visitConfigSpaceExpr(self, ctx:mdldParser.ConfigSpaceExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#omega0.
    def visitOmega0(self, ctx:mdldParser.Omega0Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#omegaN.
    def visitOmegaN(self, ctx:mdldParser.OmegaNContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#omegaFull.
    def visitOmegaFull(self, ctx:mdldParser.OmegaFullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#omegaList.
    def visitOmegaList(self, ctx:mdldParser.OmegaListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#transformExpr.
    def visitTransformExpr(self, ctx:mdldParser.TransformExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#axiomStmt.
    def visitAxiomStmt(self, ctx:mdldParser.AxiomStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#axiomKeyword.
    def visitAxiomKeyword(self, ctx:mdldParser.AxiomKeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#reflectologyStmt.
    def visitReflectologyStmt(self, ctx:mdldParser.ReflectologyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#defineStmt.
    def visitDefineStmt(self, ctx:mdldParser.DefineStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#reduceStmt.
    def visitReduceStmt(self, ctx:mdldParser.ReduceStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#computeStmt.
    def visitComputeStmt(self, ctx:mdldParser.ComputeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#evaluateStmt.
    def visitEvaluateStmt(self, ctx:mdldParser.EvaluateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#optimizeStmt.
    def visitOptimizeStmt(self, ctx:mdldParser.OptimizeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#ireStmt.
    def visitIreStmt(self, ctx:mdldParser.IreStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#dualSymmetryStmt.
    def visitDualSymmetryStmt(self, ctx:mdldParser.DualSymmetryStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#thetaExpr.
    def visitThetaExpr(self, ctx:mdldParser.ThetaExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#quotientExpr.
    def visitQuotientExpr(self, ctx:mdldParser.QuotientExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#equivRel.
    def visitEquivRel(self, ctx:mdldParser.EquivRelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#orbitExpr.
    def visitOrbitExpr(self, ctx:mdldParser.OrbitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#groupExpr.
    def visitGroupExpr(self, ctx:mdldParser.GroupExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#simplifyExpr.
    def visitSimplifyExpr(self, ctx:mdldParser.SimplifyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#composeExpr.
    def visitComposeExpr(self, ctx:mdldParser.ComposeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#lossExpr.
    def visitLossExpr(self, ctx:mdldParser.LossExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#convergeExpr.
    def visitConvergeExpr(self, ctx:mdldParser.ConvergeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#limitTarget.
    def visitLimitTarget(self, ctx:mdldParser.LimitTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#entropyExpr.
    def visitEntropyExpr(self, ctx:mdldParser.EntropyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#nonlinearExpr.
    def visitNonlinearExpr(self, ctx:mdldParser.NonlinearExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#hyperrealExpr.
    def visitHyperrealExpr(self, ctx:mdldParser.HyperrealExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#dimensionExpr.
    def visitDimensionExpr(self, ctx:mdldParser.DimensionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#goodnessExpr.
    def visitGoodnessExpr(self, ctx:mdldParser.GoodnessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#costExpr.
    def visitCostExpr(self, ctx:mdldParser.CostExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#preserveExpr.
    def visitPreserveExpr(self, ctx:mdldParser.PreserveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#energyExpr.
    def visitEnergyExpr(self, ctx:mdldParser.EnergyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#divergeExpr.
    def visitDivergeExpr(self, ctx:mdldParser.DivergeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#gradientExpr.
    def visitGradientExpr(self, ctx:mdldParser.GradientExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#dynamicsExpr.
    def visitDynamicsExpr(self, ctx:mdldParser.DynamicsExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#probExpr.
    def visitProbExpr(self, ctx:mdldParser.ProbExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#stepExpr.
    def visitStepExpr(self, ctx:mdldParser.StepExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#stabilizeExpr.
    def visitStabilizeExpr(self, ctx:mdldParser.StabilizeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#transformOp.
    def visitTransformOp(self, ctx:mdldParser.TransformOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#pathExpr.
    def visitPathExpr(self, ctx:mdldParser.PathExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#fluxExpr.
    def visitFluxExpr(self, ctx:mdldParser.FluxExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#causalExpr.
    def visitCausalExpr(self, ctx:mdldParser.CausalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#optimizeExpr.
    def visitOptimizeExpr(self, ctx:mdldParser.OptimizeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#lineageExpr.
    def visitLineageExpr(self, ctx:mdldParser.LineageExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#emergeExpr.
    def visitEmergeExpr(self, ctx:mdldParser.EmergeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#dualExpr.
    def visitDualExpr(self, ctx:mdldParser.DualExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#nlpStmt.
    def visitNlpStmt(self, ctx:mdldParser.NlpStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#patternMatchStmt.
    def visitPatternMatchStmt(self, ctx:mdldParser.PatternMatchStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#nlpProcessStmt.
    def visitNlpProcessStmt(self, ctx:mdldParser.NlpProcessStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#nlpTransformStmt.
    def visitNlpTransformStmt(self, ctx:mdldParser.NlpTransformStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#regexStmt.
    def visitRegexStmt(self, ctx:mdldParser.RegexStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#regexMatchStmt.
    def visitRegexMatchStmt(self, ctx:mdldParser.RegexMatchStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#regexReplaceStmt.
    def visitRegexReplaceStmt(self, ctx:mdldParser.RegexReplaceStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#regexExtractStmt.
    def visitRegexExtractStmt(self, ctx:mdldParser.RegexExtractStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#regexSplitStmt.
    def visitRegexSplitStmt(self, ctx:mdldParser.RegexSplitStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#abiDecl.
    def visitAbiDecl(self, ctx:mdldParser.AbiDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#abiBody.
    def visitAbiBody(self, ctx:mdldParser.AbiBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#abiMember.
    def visitAbiMember(self, ctx:mdldParser.AbiMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#apiDecl.
    def visitApiDecl(self, ctx:mdldParser.ApiDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#apiBody.
    def visitApiBody(self, ctx:mdldParser.ApiBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#apiEndpoint.
    def visitApiEndpoint(self, ctx:mdldParser.ApiEndpointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#httpMethod.
    def visitHttpMethod(self, ctx:mdldParser.HttpMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#ffiCall.
    def visitFfiCall(self, ctx:mdldParser.FfiCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#exportStmt.
    def visitExportStmt(self, ctx:mdldParser.ExportStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#importStmt.
    def visitImportStmt(self, ctx:mdldParser.ImportStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matrixStmt.
    def visitMatrixStmt(self, ctx:mdldParser.MatrixStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matrixLiteral.
    def visitMatrixLiteral(self, ctx:mdldParser.MatrixLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matrixRows.
    def visitMatrixRows(self, ctx:mdldParser.MatrixRowsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matrixRow.
    def visitMatrixRow(self, ctx:mdldParser.MatrixRowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matrixOperation.
    def visitMatrixOperation(self, ctx:mdldParser.MatrixOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matrixMul.
    def visitMatrixMul(self, ctx:mdldParser.MatrixMulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matrixAccess.
    def visitMatrixAccess(self, ctx:mdldParser.MatrixAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#typeDecl.
    def visitTypeDecl(self, ctx:mdldParser.TypeDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#typeParamsOpt.
    def visitTypeParamsOpt(self, ctx:mdldParser.TypeParamsOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#typeParamList.
    def visitTypeParamList(self, ctx:mdldParser.TypeParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#typeVar.
    def visitTypeVar(self, ctx:mdldParser.TypeVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#typeExpr.
    def visitTypeExpr(self, ctx:mdldParser.TypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#typeArgsOpt.
    def visitTypeArgsOpt(self, ctx:mdldParser.TypeArgsOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#variantDecl.
    def visitVariantDecl(self, ctx:mdldParser.VariantDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#variantBody.
    def visitVariantBody(self, ctx:mdldParser.VariantBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#variantCase.
    def visitVariantCase(self, ctx:mdldParser.VariantCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#moduleDecl.
    def visitModuleDecl(self, ctx:mdldParser.ModuleDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#moduleExpr.
    def visitModuleExpr(self, ctx:mdldParser.ModuleExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#moduleType.
    def visitModuleType(self, ctx:mdldParser.ModuleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#sigItemList.
    def visitSigItemList(self, ctx:mdldParser.SigItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#sigItem.
    def visitSigItem(self, ctx:mdldParser.SigItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#functorApp.
    def visitFunctorApp(self, ctx:mdldParser.FunctorAppContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#openStmt.
    def visitOpenStmt(self, ctx:mdldParser.OpenStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#typeList.
    def visitTypeList(self, ctx:mdldParser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#recordDecl.
    def visitRecordDecl(self, ctx:mdldParser.RecordDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#fieldDeclList.
    def visitFieldDeclList(self, ctx:mdldParser.FieldDeclListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#fieldDecl.
    def visitFieldDecl(self, ctx:mdldParser.FieldDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#funcDecl.
    def visitFuncDecl(self, ctx:mdldParser.FuncDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#paramListOpt.
    def visitParamListOpt(self, ctx:mdldParser.ParamListOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#paramList.
    def visitParamList(self, ctx:mdldParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#param.
    def visitParam(self, ctx:mdldParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#ioDecl.
    def visitIoDecl(self, ctx:mdldParser.IoDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#ioExpr.
    def visitIoExpr(self, ctx:mdldParser.IoExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#doBlock.
    def visitDoBlock(self, ctx:mdldParser.DoBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#ioStatementList.
    def visitIoStatementList(self, ctx:mdldParser.IoStatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#ioStatement.
    def visitIoStatement(self, ctx:mdldParser.IoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#assignment.
    def visitAssignment(self, ctx:mdldParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#equation.
    def visitEquation(self, ctx:mdldParser.EquationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#inequality.
    def visitInequality(self, ctx:mdldParser.InequalityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#implication.
    def visitImplication(self, ctx:mdldParser.ImplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#quantified.
    def visitQuantified(self, ctx:mdldParser.QuantifiedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#quantifier.
    def visitQuantifier(self, ctx:mdldParser.QuantifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#binderList.
    def visitBinderList(self, ctx:mdldParser.BinderListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#binder.
    def visitBinder(self, ctx:mdldParser.BinderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#probability.
    def visitProbability(self, ctx:mdldParser.ProbabilityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#formula.
    def visitFormula(self, ctx:mdldParser.FormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#disjunction.
    def visitDisjunction(self, ctx:mdldParser.DisjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#conjunction.
    def visitConjunction(self, ctx:mdldParser.ConjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#negation.
    def visitNegation(self, ctx:mdldParser.NegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#atom.
    def visitAtom(self, ctx:mdldParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#relation.
    def visitRelation(self, ctx:mdldParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#predicate.
    def visitPredicate(self, ctx:mdldParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#argList.
    def visitArgList(self, ctx:mdldParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#expr.
    def visitExpr(self, ctx:mdldParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#term.
    def visitTerm(self, ctx:mdldParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#factor.
    def visitFactor(self, ctx:mdldParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#postfix.
    def visitPostfix(self, ctx:mdldParser.PostfixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#postfixOp.
    def visitPostfixOp(self, ctx:mdldParser.PostfixOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#subscript.
    def visitSubscript(self, ctx:mdldParser.SubscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#primary.
    def visitPrimary(self, ctx:mdldParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#letExpr.
    def visitLetExpr(self, ctx:mdldParser.LetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#letBinding.
    def visitLetBinding(self, ctx:mdldParser.LetBindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#letRecExpr.
    def visitLetRecExpr(self, ctx:mdldParser.LetRecExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#recBindingList.
    def visitRecBindingList(self, ctx:mdldParser.RecBindingListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#recBinding.
    def visitRecBinding(self, ctx:mdldParser.RecBindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#ifExpr.
    def visitIfExpr(self, ctx:mdldParser.IfExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#elifChain.
    def visitElifChain(self, ctx:mdldParser.ElifChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#elifClause.
    def visitElifClause(self, ctx:mdldParser.ElifClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matchExpr.
    def visitMatchExpr(self, ctx:mdldParser.MatchExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matchCases.
    def visitMatchCases(self, ctx:mdldParser.MatchCasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#matchCase.
    def visitMatchCase(self, ctx:mdldParser.MatchCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#guardOpt.
    def visitGuardOpt(self, ctx:mdldParser.GuardOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#pattern.
    def visitPattern(self, ctx:mdldParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#patternAtom.
    def visitPatternAtom(self, ctx:mdldParser.PatternAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#patternSuffix.
    def visitPatternSuffix(self, ctx:mdldParser.PatternSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#patternList.
    def visitPatternList(self, ctx:mdldParser.PatternListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#fieldPatternList.
    def visitFieldPatternList(self, ctx:mdldParser.FieldPatternListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#fieldPattern.
    def visitFieldPattern(self, ctx:mdldParser.FieldPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#tryExpr.
    def visitTryExpr(self, ctx:mdldParser.TryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#raiseExpr.
    def visitRaiseExpr(self, ctx:mdldParser.RaiseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#setComprehension.
    def visitSetComprehension(self, ctx:mdldParser.SetComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#tupleExpr.
    def visitTupleExpr(self, ctx:mdldParser.TupleExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#exprList.
    def visitExprList(self, ctx:mdldParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#lambdaExpr.
    def visitLambdaExpr(self, ctx:mdldParser.LambdaExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#recordExpr.
    def visitRecordExpr(self, ctx:mdldParser.RecordExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#fieldList.
    def visitFieldList(self, ctx:mdldParser.FieldListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#field.
    def visitField(self, ctx:mdldParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#funcCall.
    def visitFuncCall(self, ctx:mdldParser.FuncCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#lvalue.
    def visitLvalue(self, ctx:mdldParser.LvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#lvalueSuffix.
    def visitLvalueSuffix(self, ctx:mdldParser.LvalueSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mdldParser#comment.
    def visitComment(self, ctx:mdldParser.CommentContext):
        return self.visitChildren(ctx)



del mdldParser