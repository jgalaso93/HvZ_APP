import os

# General folder where databases are stored
database_folder = 'D:\\Proyectos\\HvZ\\HvZ PvE\\HvZ_APP\\databases'

# General database of players
player_db_file = os.path.join(database_folder, 'database.csv')

# Database where NPC influence reactions are
npc_db_file = os.path.join(database_folder, 'NPC_database.csv')
npc_db_file_w2 = os.path.join(database_folder, 'NPC_database_w2.csv')

# Database where general team info is stored
teams_db_file = os.path.join(database_folder, 'teams_database.csv')

# Database of missions (title, id, hints, answers...)
missions_db_file = os.path.join(database_folder, 'mission_database.csv')

# Database for the general conversation with the bot
conversation_db_file = os.path.join(database_folder, 'conversation_database.csv')

# Database for the general conversation with the bot
npc_conversation_db_file = os.path.join(database_folder, 'NPC_conversation_database.csv')
