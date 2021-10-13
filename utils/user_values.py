def all_active_missions(df, user_id):
    """
    For a given user_id returns all the active missions as a list of strings
    """
    active_missions = []
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Aulari'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Carpa'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Civica'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Comunicacio'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Sud'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Nord'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Central'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_ETSE'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_FTI'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Med'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_SAF'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EC'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Torres'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Vet'])
    active_missions = list(filter(lambda x: x != ' ', active_missions))
    return active_missions


def all_done_missions(df, user_id):
    """
    For a given user_id returns all the done missions as a list of strings
    """
    done_missions = []
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Aulari'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Carpa'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Civica'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Comunicacio'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Sud'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Nord'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Central'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_ETSE'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_FTI'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Med'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_SAF'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EC'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Torres'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Vet'])
    done_missions = list(filter(lambda x: x != ' ', done_missions))
    final_missions = []
    for ms in done_missions:
        missions_subset = ms.split(", ")
        for mis in missions_subset:
            final_missions.append(mis)
    return final_missions


def amount_of_missions_done(df, user_id):
    """
    For a given user_id returns the amount of missions done by this user
    """
    amount_missions = 0
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Aulari']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Carpa']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Civica']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Comunicacio']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Sud']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Nord']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Central']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_ETSE']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_FTI']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Med']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_SAF']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_EC']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Torres']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Vet']
    return amount_missions.values[0]


def user_points(df, user_id):
    """
    For a given user_id returns the amount of points achieved due to missions
    """
    total_points = 0
    total_points += df[df['BOT_ID'] == user_id]['P_Aulari']
    total_points += df[df['BOT_ID'] == user_id]['P_Carpa']
    total_points += df[df['BOT_ID'] == user_id]['P_Civica']
    total_points += df[df['BOT_ID'] == user_id]['P_Comunicacio']
    total_points += df[df['BOT_ID'] == user_id]['P_EB_Sud']
    total_points += df[df['BOT_ID'] == user_id]['P_EB_Nord']
    total_points += df[df['BOT_ID'] == user_id]['P_EB_Central']
    total_points += df[df['BOT_ID'] == user_id]['P_ETSE']
    total_points += df[df['BOT_ID'] == user_id]['P_FTI']
    total_points += df[df['BOT_ID'] == user_id]['P_Med']
    total_points += df[df['BOT_ID'] == user_id]['P_SAF']
    total_points += df[df['BOT_ID'] == user_id]['P_EC']
    total_points += df[df['BOT_ID'] == user_id]['P_Torres']
    total_points += df[df['BOT_ID'] == user_id]['P_Vet']
    return total_points.values[0]


def holiwi(update, context):
    update.message.reply_text("holiwi")