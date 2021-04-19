#!/usr/bin/env python

import waterqualityapp

class MainHandler(waterqualityapp.RequestHandler):
    def get(self):
        self.response.write('I update automatically!')

app = waterqualityapp.WSGIApplication([
    ('/', MainHandler)
], debug=True)