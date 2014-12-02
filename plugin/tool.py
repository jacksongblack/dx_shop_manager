def get_users_groups_to_string(users):
    for user in users:
        group_str = ''
        for group in user.groups.all():
            group_str += group.name
        user.groups_str = group_str
    return users
