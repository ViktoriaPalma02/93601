import validators 
import whois

"""
Function to evaluate domain values in url
"""
def ev_url(url_input):
    domain = whois.whois(url_input)

    ev_url.domain_name = list(map(domain.get, ["domain_name"]))
    creation_domain = list(map(domain.get,["creation_date"]))
    update_domain = list(map(domain.get, ["updated_date"]))

    if domain.get("domain_name") is not None:
        domain_registerd = True
    else:
        domain_registerd = False
        creation_domain = 0
        update_domain = 0

    print(ev_url.domain_name)


"""
function that verifies if domain is registered

"""
def ev_domain(domain_name):
    try:
        test = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(test.domain_name)

#Evaluate if user inputs a URL
print("input a URL")
user_input = input()

validate_url = validators.url(user_input)
if validate_url:    
    print("This is a Url")
    evaluate = ev_url(user_input)
else:
    print("not a url")

#print(ev_url.domain_name)
a = ev_url.domain_name[0]
#print(a)
b = a[0]
#print(b)

print(b, "is registered" if ev_domain(b) else "is not registerd")
