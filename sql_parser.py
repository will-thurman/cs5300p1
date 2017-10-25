from lark import Lark

grammar = '''

  query: s_clause f_clause [w_clause]

  s_clause: "SELECT" expr [("," expr)*]

  f_clause: "FROM" REL [("," REL)*]

  w_clause: "WHERE" c_expr [ (("AND"|"OR") c_expr)* [("IN"|"EXISTS"|"NOT EXISTS"]]

  gb_clause:

  h_clause:

  ob_clause:
  
  expr: bool_expr
      | num_expr

  bool_expr: ATTR COMP ATTR
      
  c_expr: ATTR COMP ATTR

  attr_list: ATTR [("," ATTR)*]

  ATTR: (LETTER)+ ["." (LETTER)+]

  REL: (LETTER)+ [ (AS (LETTER)+)*]

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

  %import common.LETTER
  %import common.
  %import common.DIGIT
  %import common.WS
  %ignore WS
'''