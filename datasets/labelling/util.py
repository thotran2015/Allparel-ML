
# Two labels are equal if they are the same without whitespace
def are_equal(s1, s2):
    if s1 == s2:
        return True
    if s1.replace(' ', '') == s2.replace(' ',''):
        return True
    return False


