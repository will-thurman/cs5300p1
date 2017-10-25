from lark import Lark, Transformer

query_grammar = r'''

  query: f_clause

  s_clause: "SELECT" num_expr ("," num_expr)*

  f_clause: "FROM" REL ("," REL)*

  w_clause: "WHERE" expr (("AND"|"OR") expr)* (("AND"|"OR")? ("IN"|"EXISTS"|"NOT IN"|"NOT EXISTS") query)*

  gb_clause: "TODO"

  h_clause: "TODO"

  ob_clause: "TODO"
  
  expr: bool_expr
      | num_expr

  bool_expr: ATTR ((COMP ATTR)|(COMP CONST))*

  num_expr: ATTR ((OPER ATTR)|(OPER CONST))*

  ATTR: CNAME | CNAME "." CNAME | 

  REL: ((CNAME)|(CNAME "AS" CNAME)|(CNAME CNAME))

  CONST: STRING
       | INT 

  OPER: "+"
      | "-"
      | "*"
      | "/"

  COMP: "="
      | ">"
      | "<"
      | ">="
      | "<="
      | "<>"

  AGGR_FUN: "SUM(" ATTR ")"
          | "COUNT(" ATTR ")"
          | "MIN(" ATTR ")"
          | "MAX(" ATTR ")"
          | "AVG(" ATTR ")"

  %import common.CNAME
  %import common.ESCAPED_STRING -> STRING
  %import common.SIGNED_INT -> INT
  %import common.WS
  %ignore WS
'''

def parse(text):
  """ Parses sql and returns the resulting tree"""
  sql_parser = Lark(query_grammar, start="query")
  return sql_parser.parse(text.upper())

