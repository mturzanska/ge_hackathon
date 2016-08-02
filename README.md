# Peacemaker

### About

The world around us is a noisy one. From the our always-on mobile devices to our open plan offices, we are bathing in a sea of constant noise. It's impacting out ability to [sleep, reason, and work effectively][1]. Due to how sound permeates our surroundings it's usually impossible to nullify it.

Peacemaker is a web application that will show you the quickest way to get to a quiet location to let your brain rest. It does this by tapping into GE's Intelligent Cities API that provides access to smart streetlights - streetlights that are outfitted with sensors to to record sound, take pictures, count pedestrians and cars, and much more.

### State of the Project

The project is currently in a working alpha version. Use interaction is limited to clicking a button that will submit the user's current location to app for processing. Afterwards, the app will query GE's datastores for information about pedestrian counts as well as audio files from sensors near the user. The audio files will be processed to discern k the noise level at each sensor's location. Finally, this data will be combined and a map displayed to the user showing the shortest path to the quietest area.

There are some constraints, chief among them the limited number of streetlight sensors (12) made available to [hackathon][2] participants. Due to this, the current application works only within about a 5km radius around San Diego's downtown area. To sidestep this requirement during development and testing, it is possible to hardcode the user's location to something like (32.713765, -117.156406).

### Set up

The application is fairly easy to set up. You will require access to Predix and the ability to create the required services: Public Safety, Pedestrian, and Authentication. On top of that, you'll required a google maps API key to use to display the map.

Set up steps:

1. git clone the repository.
2. `pip install -r requirments.txt`
3. Take a look at the `api/conf.py.sample` file to see how to provide the Predix API keys. In production, `conf.py` should build the settings dictionary out of environment variables, but while in development you may hardcode them for ease of use.
4. Set the `GOOGLE_API_KEY` environment variable to the google api key.
5. Launch the app with `cd peacemaker && FLASK_APP=__init__.py flask run`
6. Open your browser and navigate to `localhost:5000`

[1]: http://nautil.us/issue/38/noise/this-is-your-brain-on-silence-rp
[2]: http://intelligentworld.devpost.com
