class NPC(object):
    def __init__(self):
        """
        Attributes:
            inclination: (int)
            Value that determines the inclination of the NPC. 0 means neutral,
            positive means favorable to Corruptus, negative means favorable to
            Anomalis. Use database to update!
        """
        self.inclination = 0


class DianeFossey(NPC):
    @staticmethod
    def max_corruptus(self):
        return "TEXT MAX CORRUPTUS"

    @staticmethod
    def high_corruptus(self):
        return "TEXT HIGH CORRUPTUS"

    @staticmethod
    def medium_corruptus(self):
        return "TEXT MEDIUM CORRUPTUS"

    @staticmethod
    def low_corruptus(self):
        return "TEXT LOW CORRUPTUS"

    @staticmethod
    def neutral(self):
        return "TEXT NEUTRAL"

    @staticmethod
    def low_anomalis(self):
        return "TEXT LOW ANOMALIS"

    @staticmethod
    def medium_anomalis(self):
        return "TEXT MEDIUM ANOMALIS"

    @staticmethod
    def high_anomalis(self):
        return "TEXT HIGH ANOMALIS"

    @staticmethod
    def max_anomalis(self):
        return "TEXT MAX ANOMALIS"

    @staticmethod
    def general_lore(self):
        return "GENERAL LORE"

    @staticmethod
    def who_am_i(self):
        return "WHO AMB I TEXT"
