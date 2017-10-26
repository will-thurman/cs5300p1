%{
#include <iostream>
using namespace std;

  // Things from Flex that Bison needs to know
extern int yylex();
extern int line_num;
extern char* yytext;

  // Prototype for Bison's error message function
int yyerror(const char *p);
%}

%token T_COL
%token T_NUM
%token T_STR
%token T_ARTH_OP
%token T_COMP_OP

%token K_CHAIN
%token K_SEL
%token K_FRM
%token K_WHR
%token K_GBY
%token K_HVG
%token K_OBY
%token K_UNI
%token K_INT
%token K_AS
%token K_IN
%token K_CON
%token K_EXS
%token K_LPAR
%token K_RPAR
%token K_COM
%token K_AGR
%token K_EXC

%% /* Grammar */

querySeq: query
	| query K_UNI querySeq
	| query K_INT querySeq
	| query K_CON querySeq
	| query K_EXC querySeq
	;

query: sClause fClause
	| sClause fClause wClause
	| sClause fClause wClause gClause
	| sClause fClause wClause gClause hClause
	| K_LPAR query K_RPAR
	;
	
sClause: K_SEL colList
	;
	
fClause: K_FRM relList
	;

	
wClause: K_WHR condList
	| K_WHR condList K_IN K_LPAR querySeq K_RPAR
	| K_WHR condList K_EXS K_LPAR querySeq K_RPAR
	;
	
gClause: K_GBY colList
	;

hClause: K_HVG condList
	;

oClause: K_OBY colList

relList: T_COL
	| T_COL T_COL
	| T_COL K_AS T_COL
	| T_COL T_COL K_COM relList
	| T_COL K_COM relList
	| T_COL K_AS T_COL K_COM relList
	;

colList: expr
	| expr K_AS T_COL
	| K_AGR K_LPAR expr K_RPAR
	| K_AGR K_LPAR expr K_RPAR K_AS T_COL
	| K_AGR K_LPAR expr K_RPAR K_COM colList
	| K_AGR K_LPAR expr K_RPAR K_AS T_COL K_COM colList
	| expr K_AS T_COL K_COM colList
	| expr K_COM colList
	;

condList: c_expr
	| c_expr K_CHAIN condList
	;

expr: const
	| const T_ARTH_OP const
	| const T_ARTH_OP const expr
	;

c_expr: expr
	| expr T_COMP_OP const
	| expr T_COMP_OP K_LPAR query K_RPAR
	| const T_COMP_OP expr
	| K_AGR K_LPAR expr K_RPAR T_COMP_OP const
	| const T_COMP_OP K_AGR K_LPAR expr K_RPAR
	| const T_COMP_OP K_LPAR query K_RPAR
	;

const: T_NUM
	| T_STR
	| T_COL
	;

%%
int yyerror(const char *p)
{
  cout << "ERROR: with token \'" << yytext << "\'" << endl;
}

int main()
{
  int failcode;
  cout << "Parsing SQL..." << endl;
  failcode = yyparse();

  if (failcode)
    cout << "INVALID SQL!" << endl;
  else
    cout << "VALID SQL" << endl;
  return 0;
}