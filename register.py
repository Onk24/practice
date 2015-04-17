import os
import webapp2
import jinja2
import re

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)



class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
class Reg(db.Model):
	ids = db.StringProperty(required=True)
	name = db.StringProperty(required=True)
	department = db.StringProperty(required=True) 	
	time=db.DateTimeProperty(auto_now_add=True)

NAME_RE = re.compile(r"^[a-zA-Z_-]{3,20}$")
def valid_name(name):
    return name and NAME_RE.match(name)

class MainPage(Handler):
	def render_front(self,ids="", name="",error_name="",department="",
							error=""):
		regx=db.GqlQuery("SELECT * FROM Reg ORDER BY time DESC")
		
		self.render("front.html", ids=ids,
					name=name,error_name=error_name,department=department,
					error=error,regx=regx)
	def get(self):
		self.render_front()
	def post(self):
		ids = self.request.get("ids")
		name = self.request.get("name")
		department = self.request.get("department")
	
		
	
		
		if ids and name and department:
			if not valid_name(name):
				error_name="Invalid name"
				self.render_front(ids,name,error_name,department)
			else:
				a= Reg(ids=ids,name=name,department=department)
				a.put()
				self.redirect('/')
		else:
			error = "Invalid entry"
			error_name=""
			self.render_front(ids,name,error_name,department,error)


app = webapp2.WSGIApplication([('/', MainPage)],
								debug=True)
