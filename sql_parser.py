from lark import Lark, Transformer, common
import sys

query_grammar = r'''
  
  queryseq: query (["UNION"|"INTERSECT"|"EXCEPT"|"CONTAINS"] query)*

  query: sclause fclause
    | sclause fclause wclause
    | sclause fclause gclause
    | sclause fclause wclause gclause
    | sclause fclause wclause gclause hclause
    | query oclause
    | "(" query ")"

  sclause: "SELECT" _attrlist

  fclause: "FROM" _rellist

  wclause: "WHERE" _condlist

  gclause: "GROUP BY" _attrlist

  hclause: "HAVING" _condlist

  oclause: "ORDER BY" _attrlist

  _attrlist: _expr
  	| _expr "AS" _expr
	  | _expr "," _attrlist
	  | _expr "AS" attr "," _attrlist

  _rellist: rel ("," rel)*

  _condlist: cexpr
  	| cexpr ("AND"|"OR") _condlist

  _expr: attr
  	| const
	  | const a_ops _expr
	  | _expr a_ops const
	  | "(" _expr ")"

  cexpr: _expr _c_ops _expr
  	| _expr _c_ops ["("] queryseq [")"]
	  | agr _c_ops _expr
	  | _expr _c_ops agr

  attr: ident | ident dot ident | ident "AS" ident | agr | agr "AS" ident
  	| "*"

  rel: ident | ident ident | ident "AS" ident

  a_ops: AOPS

  AOPS: "+" | "-" | "*" | "/"

  _c_ops: "=" | ">" | "<" | "<>" | ">=" | "<=" | "IN"

  agr: AGR "(" _expr ")"

  AGR: "SUM" | "COUNT" | "MIN" | "MAX" | "AVE"

  const: num
	| string

  ident: CNAME

  string: /\"[^\"]*\"/|/'[^']*'/|/‘|[^’]*’/
  
  num: ("+"|"-")? NUMBER

  dot: DOT

  DOT: "."

  %import common.CNAME 
  %import common.NUMBER
  %import common.WS
  %ignore WS
'''

def parse(text):
  """ Parses sql and returns the resulting tree"""
  sql_parser = Lark(query_grammar, start="queryseq")
  return sql_parser.parse(text.upper())

class ToDict(Transformer):
  def queryseq(self, items):
    return items
  def query(self, items):
    q = {}
    if len(items) > 1:
      for i in items:
        q[i[0]] = i[1]
      return q
    return items[0]
  def sclause(self, items):
    return 'sclause', items
  def fclause(self, items):
    return 'fclause', items
  def wclause(self, items):
    return 'wclause', items
  def gclause(self, items):
    return 'gclause', items
  def hclause(self, items):
    return 'hclause', items
  def oclause(self, items):
    return 'oclause', items
  def attr(self, items):
    if len(items) == 3:
      return "{}.{}".format(items[0],items[2])
    elif len(items) == 2:
      return items[0], items[1]
    elif len(items) == 0:
      return '*'
    return items[0]
  def rel(self, items):
    if len(items) == 2:
      return items[0], items[1]
    return items[0]
  def cexpr(self, items):
    return items[0], items[1]
  def ident(self, i):
    return i[0].value
  def num(self, n):
    return int(n[0].value)
  def string(self, s):
    return s[0].value
  def agr(self, a):
    return a[0].value, a[1]
  def const(self, c):
    return c[0]

def fclause_check(query):
  
  return True

def semantic_analysis(d):
  table_aliases = {}
  tables = []
  selected = []
  attr_aliases = {}
  tables_attrs = {}
  query_type = None
  for query in d:

    if 'fclause' in query:
      for rel in query['fclause']:
        alias = ""
        if len(rel) == 2:
          alias = rel[1].lower()
          table = rel[0].lower()
        else:
          table = rel.lower()
        if table.lower() not in TABLES:
          print(table, "is not a valid table, stopping analysis")
          sys.exit(1)
        if alias != "":
          table_aliases[alias] = table

        tables.append(table)
        tables_attrs[table] = TABLES[table].keys()
      print("FROM clause correct")

    
    if 'sclause' in query:
      for attr in query['sclause']:
        agr = ""
        found = False
        alias = ""
        rtable = ""
        if type(attr) is tuple:
          alias = attr[1]
          attribute = attr[0]
          if type(attribute) is tuple:
            agr = attribute[0]
            attribute = "{}({})".format(agr, attribute[1])
        elif '.' in attr:
          rtable, attribute = attr.split('.')
        else:
          attribute = attr
        attribute = attribute.lower()
        rtable = rtable.lower()
        alias = alias.lower()
        if rtable:
          if rtable not in tables and rtable not in table_aliases:
            print(rtable, "is not a valid relation, stopping analysis")
            sys.exit(1)
        if alias:
          attr_aliases[alias] = attribute

        if '*' in attribute:
          found = True

        for t_attrs in tables_attrs:
          if attribute in tables_attrs[t_attrs]:
            found = True
            selected.append((t_attrs, attribute))
            break

        if not found:
          print(attribute, "is not a valid attribute in this query, stopping analysis")
          sys.exit(1)

        if len(selected) == 1:
          query_type = TABLES[selected[0][0]][selected[0][1]]
        print("Select clause ok")

    if 'wclause' in query:
      for cond in query['wclause']:
        lhs_type = None
        rhs_type = None
        rtables = ""
        l_rtable = ""
        rconst = False
        lconst = False
        rhs = cond[0]
        lhs = cond[1]
        if type(rhs) is str:
          rhs = rhs.lower()
        if type(lhs) is list and type(lhs[0]) is dict:
          lhs_type = semantic_analysis(lhs)
        elif type(lhs) is str:
          lhs = lhs.lower()

        if '.' in rhs:
          rtable, attribute = rhs.split('.')
        else:
          attribute = rhs

        if type(lhs) is str and '.' in lhs:
          l_rtable, l_attribute = lhs.split('.')
        else:
          l_attribute = lhs

        if type(rhs) is int:
          rhs_type = 'integer'
          rconst = True
          found = True
        elif '\'' in rhs or '"' in rhs:
          rhs_type = 'string'
          rconst = True
          found = True

        if type(lhs) is int:
          lhs_type = 'integer'
          lconst = True
          l_found = True
        elif '\'' in lhs or '"' in rhs:
          lhs_type = 'string'
          lconst = True
          l_found = True

        if rtable:
          if rtable not in tables and rtable not in table_aliases and not rconst:
            print(rtable, "is not a valid relation in comparison, stopping analysis")
            sys.exit(1)
        if l_rtable:
          if l_rtable not in tables and l_rtable not in table_aliases and not lconst:
            print(l_rtable, "is not a valid relation in comparison, stopping analysis")
            sys.exit(1)

        if not rconst:
          for t_attrs in tables_attrs:
            if attribute in tables_attrs[t_attrs]:
              found = True
              rhs_ref = (t_attrs, attribute)
              break

        if not lconst:
          for t_attrs in tables_attrs:
            if l_attribute in tables_attrs[t_attrs]:
              l_found = True
              lhs_ref = (t_attrs, l_attribute)
              break

        if not found:
          print(attribute, "is not a valid attribute in comparison, stopping analysis")
          sys.exit(1)
        if not l_found:
          print(l_attribute, "is not a valid attribute in comparison, stopping analysis")
          sys.exit(1)
        if not rconst:
          rhs_type = TABLES[rhs_ref[0]][rhs_ref[1]]
        if not lconst:
          lhs_type = TABLES[lhs_ref[0]][lhs_ref[1]]
        if rhs_type != lhs_type:
          print("Invalid comparison between", rhs_type, "and", lhs_type, "stopping analysis")
          sys.exit(1)
      print("Where clause good to go")
    if 'gclause' in query:
      pass # TODO
    if 'hclause' in query:
      pass # TODO

  return query_type

def main():
  global TABLES
  TABLES = {
    'sailors' : {
      'sid' : 'integer',
      'sname' : 'string',
      'rating' : 'integer',
      'age' : 'real'
    },
    'boats' : {
      'bid': 'integer',
      'bname': 'string',
      'color': 'string'
    },
    'reserves' : {
      'sid': 'integer',
      'bid': 'integer',
      'day': 'string'
    }
  }

  print("Reading...")
  query = sys.stdin.read()
  try:
    tree = parse(query)
    print("Valid query!")
  except common.ParseError:
    print("Could not parse the query.")
    sys.exit(1)
  print("Performing semantic analysis...")
  parsed = ToDict().transform(tree)
  semantic_analysis(parsed)

if __name__ == "__main__":
  main()
