from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"

                output += "<a href = /restaurants/new >Add a new restaurant</a>"
                output += "</br>"
                output += "</br>"

                output += "<h2  >Restaurants List</h1>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href = /restaurants/%s/edit > Edit </a>" %restaurant.id
                    output += "</br>"
                    output += "<a href = /restaurants/%s/delete > Delete </a>" %restaurant.id
                    output += "</br>"
                    output += "</br>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output =  ""
                output += "<html><body>"
                output += '''<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>'''
                output += ''' <h2>Add a new restaurant</h2><input name ="restaurant" type = "text" placeholder="Restaurant name">'''
                output +=''' <input type="submit" value="Create"> </form>'''

                output += "</html></body>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurant_id = self.path.split("/")[2]
                target_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                if (target_restaurant!=0):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%s/edit'>" %  restaurant_id
                    output += "<input name = 'edit_restaurant' type = 'text' placeholder = 'Edit %s '>" % target_restaurant.name
                    output += "<input type='submit' value='Create'></form>"

                    output += "</html></body>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                target_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                if (target_restaurant!=0):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>Delete %s ?</h1>" %target_restaurant.name
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" %  restaurant_id
                    output += "<input type='submit' value='Delete'></form>"

                    output += "</html></body>"

                self.wfile.write(output)
                print output
                return


            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    addedrestaurant = fields.get('restaurant')
                    newRestaurant = Restaurant(name=addedrestaurant[0])
                    session.add(newRestaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                print restaurant_id
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                targetRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                if (targetRestaurant!=0):
                    session.delete(targetRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                restaurant_id = self.path.split("/")[2]
                print restaurant_id
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    editRestaurant = fields.get('edit_restaurant')

                    targetRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                    if (targetRestaurant!=0):
                        targetRestaurant.name = editRestaurant[0]
                        session.add(targetRestaurant)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()


                    # messagecontent = fields.get('message')

            # output = ""
            # output += "<html><body>"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> %s </h1>" % messagecontent[0]
            # output += '''<form method='POST' enctype='multipart/form-data' action='/hola'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #
            # output += "</body></html>"
            # self.wfile.write(output)
            # print output
            return
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
