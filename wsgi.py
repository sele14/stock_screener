# import the app variable from the init file
# from flask_webapp import create_app

# app = create_app()

# # running the server   
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)



#####
"""Application entry point."""
from flask_webapp import create_app


def main():
    app = create_app()
    app.run(host='0.0.0.0', port=50001, debug=True)


if __name__ == "__main__":
    main()