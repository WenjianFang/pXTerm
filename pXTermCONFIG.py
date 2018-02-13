
class pXTermCONFIG:
    def __init__(self, configFile = 'sessions'):
        self.configs = configFile

    def dump_configs(self):
        with open(self.configs, 'r') as sessionFile:
            ss = sessionFile.readlines()
            for i in range(0, len(ss)):
                ss[i] = ss[i].strip('\n')

        return ss

    def write_config(self, session):
        ss = self.dump_configs()
        for s in ss:
            if s.split(' ')[0] == session[0]:
                return False

        sessionString = ''
        with open(self.configs, 'ab+') as sessionFile:
            for i in range(0, len(session)):
                if i != (len(session) - 1):
                    sessionString = sessionString + session[i] + ' '
                else:
                    sessionString = sessionString + session[i] + '\n'
            sessionFile.write(sessionString)
        return True

    def get_config_by_session_name(self, sessionName):
        ss = self.dump_configs()
        for session in ss:
            if session.split(' ')[0] == sessionName:
                return session.split(' ')

    def get_all_sessions_name(self):
        sessionsName = []
        ss = self.dump_configs()
        for session in ss:
            sessionsName.append(session.split(' ')[0])
        return sessionsName