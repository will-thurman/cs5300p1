from lark import Lark, Transformer

query_grammar = '''

  query: s_clause

  s_clause: "SELECT" expr [("," expr)*]

  f_clause: "FROM" REL [("," REL)*]

  w_clause: "WHERE" expr [ (("AND"|"OR") expr)* (("IN"|"EXISTS"|"NOT IN"|"NOT EXISTS") query)*]]

  gb_clause:

  h_clause:

  ob_clause:
  
  expr: bool_expr
      | num_expr

  bool_expr: ATTR COMP ATTR

  num_expr: ATTR [ (OPER ATTR)*]

  ATTR: (LETTER)+ ["_"] ["." (LETTER)+]

  REL: (LETTER)+ ["_"] (LETTER)* [ (AS (LETTER)+)*]

  CONST: STRING
       | INT
       | 

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
  %import common.ESCAPED_STRING -> STRING
  %import common.SIGNED_INT -> INT
  %import common.WS
  %ignore WS
'''

def parse(text):
  """ Parses sql and returns the resulting tree"""
  sql_parser = Lark(query_grammar, start="query")
  return sql_parser.parse
