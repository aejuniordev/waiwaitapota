from waiwaitapota import app
from starting_cfg import create_starting

if __name__ == '__main__':
    create_starting()
    app.run(debug=False, threaded=True)

# https://yasoob.me/posts/how-to-setup-and-deploy-jwt-auth-using-react-and-flask/
# https://github.com/vimalloc/flask-jwt-extended/issues/240
# https://dev.to/brandonwallace/deploy-flask-the-easy-way-with-gunicorn-and-nginx-jgc
# https://docs.digitalocean.com/tutorials/app-deploy-flask-app/
# https://flask.palletsprojects.com/en/2.2.x/deploying/gunicorn/