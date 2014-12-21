CONFIG_INI = "config.ini"

def load():
    config_dict = {}
    inifile = open(CONFIG_INI, "r")
    lines = inifile.readlines()
    for line in lines:
        if not line:
            continue
        (key, value) = line.split("=")
        config_dict[key] = value.strip()
    inifile.close()
    return config_dict

def reload(config_dict):
    inifile = open(CONFIG_INI, "w")
    for key in config_dict:
        value = config_dict[key]            
        inifile.write("%s=%s\n" % (key, value))
        inifile.flush()
    inifile.close()
    
def add(key, value):
    try:
        config_dict = load()
        config_dict[key] = value
        reload(config_dict)
    except IOError:
        # writing for the first time
        inifile = open(CONFIG_INI, "w")
        inifile.write("%s=%s\n" % (key, value))
        inifile.flush()
        inifile.write
        inifile.close()

def get(key):
    config_dict = load()
    return config_dict[key]
    
    