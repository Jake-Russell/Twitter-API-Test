import twint

c = twint.Config()
c.Search = ['Liz Truss']
c.Limit = 100
c.Lang = 'en'
c.Store_json = True
c.Output = "twint_json_output.json"


twint.run.Search(c)
