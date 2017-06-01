import web

urls = ('/(.*)', 'Index', 'Single', 'Work', 'Contact')

app = web.application(urls, globals())

web.config.debug = True


class Index:

	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, name=None):
		t = ['1', '2', '3']
		return self.render.index(t)

	def POST(self, name):
		return "post"

if __name__=='__main__':
	app.run()
