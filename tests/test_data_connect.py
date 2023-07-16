from data.connect import config


for environment_variable in ():

    assert environment_variable in config.keys("DECAF", "SPACES_SECRET", "APIKEY")