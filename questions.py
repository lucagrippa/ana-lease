

def get_lease_summary_questions():
# Lease Summary
# - Rent: $$$
# - Security Deposit: $$$
# - Length or date of lease:
# - address
# - Renewal information
# - Pets allowed or not
# - Utilities info
# - Furnished
# - Landlord show up notice
# - Renters insurance
    questions = [
        """Respond to the question with only a number followed by 'per month'. 
If you cannot find the answer in the context respond with N/A.
QUESTION: How much is the rent?
ANSWER: $1,400 per month

QUESTION: How much is the rent?
ANSWER: N/A

QUESTION: How much is the rent?
ANSWER:""".strip(),

"""Respond to the question with only a number.
If you cannot find the answer in the context respond with N/A.
QUESTION: How much is the security deposit?
ANSWER: $1,400

QUESTION: How much is the security deposit?
ANSWER: N/A

QUESTION: How much is the security deposit?
ANSWER:""".strip(),

"""Respond to the question with the number of months.
If you cannot find the answer in the context respond with N/A.
QUESTION: What is the length of the lease?
ANSWER: 12 months

QUESTION: What is the length of the lease?
ANSWER: N/A

QUESTION: What is the length of the lease?
ANSWER:""".strip(),

"""Respond to the question with an address.
If you cannot find the answer in the context respond with N/A.
QUESTION: What is the address of the apartment?
ANSWER: 58 East Midland Ave, Paramus, NJ

QUESTION: What is the address of the apartment?
ANSWER: N/A

QUESTION: What is the address of the apartment?
ANSWER:""".strip(),

"""Respond to the question with a 'Yes' or 'No'.
If you cannot find the answer in the context respond with N/A.
QUESTION: Will I have the ability to renew my lease?
ANSWER: Yes

QUESTION: Will I have the ability to renew my lease?
ANSWER: N/A

QUESTION: Will I have the ability to renew my lease?
ANSWER:""".strip(),

"""Respond to the question with a 'Yes' or 'No'.
If you cannot find the answer in the context respond with N/A.
QUESTION: What is the pet fee?
ANSWER: Yes

QUESTION: What is the pet fee?
ANSWER: N/A

QUESTION: What is the pet fee?
ANSWER:""".strip(),

"""Respond to the question with a list of utilities'.
If you cannot find the answer in the context respond with N/A.
QUESTION: Are any utilities included?
ANSWER: - electric
- water

QUESTION: Are any utilities included?
ANSWER: N/A

QUESTION: Are any utilities included?
ANSWER:""".strip(),

"""Respond to the question with a 'Yes' or 'No'.
If you cannot find the answer in the context respond with N/A.
QUESTION: Is the aparment furnished?
ANSWER: Yes

QUESTION: Is the aparment furnished?
ANSWER: N/A

QUESTION: Is the aparment furnished?
ANSWER:""".strip(),

"""Respond to the question with a 'Yes' or 'No'.
If you cannot find the answer in the context respond with N/A.
QUESTION: Do I need renters insurance?
ANSWER: Yes

QUESTION: Do I need renters insurance?
ANSWER: N/A

QUESTION: Do I need renters insurance?
ANSWER:""".strip(),

"""Respond to the question with a 'Yes' or 'No'.
If you cannot find the answer in the context respond with N/A.
QUESTION: Are there late fees if I do not pay rent on time?
ANSWER: Yes, $35 for every day you are late.

QUESTION: Are there late fees if I do not pay rent on time?
ANSWER: N/A

QUESTION: Are there late fees if I do not pay rent on time?
ANSWER:""".strip(),
    ]

    summary_questions = [
        "How much is rent? Give only the number.",
        "How much is the security deposit? Give only the number.",
        "What is the length of the lease? Give only the number.",
        "What is the address of the apartment? Answer with only the address",
        "Will I have the ability to renew my lease? Answer yes or no",
        "What is the pet fee? If there is, give only the number. If no, say no.",
        "Are any utilities included? List the utilities that are included.",
        "Is the aparment furnished? Answer with yes or no.",
        "Do I need renters insurance? ANswer with yes or no",
        "Are there late fees if I do not pay rent on time? Give only the number."
    ]

    titles = [
        "Rent",
        "Security Deposit",
        "Lease Duration",
        "Address",
        "Renewal",
        "Pets",
        "Utilities",
        "Furnished",
        "Renters Insurance",
        "Late Fees"
    ]

    return questions, titles


def get_counsel_questions():
    questions = [
    "Are there any references to “objectionable conduct” in the lease? What are the consequences for the objectionable conduct?",
    "For what reasons can the landlord terminate the lease early?",
    "Can the tenant ever terminate the lease? When can the tenant terminate the lease?",
    "Are the any fees listed on the lease that the landlord can charge the tenant with?",
    "Is the tenannt liable for negligence?",
    "Is the tenant being asked to indemnify the landlord for anything?",
    "Is there a confidentiality requirement anywhere in the lease?",
    "Does the lease include a lead paint disclosure?",
    "Can the tenant sublet the apartment?"
    ]

    titles = [
        "Objectionable Conduct",
        "Landlord Early Termination",
        "Tenant Early Termination"
        "Fees",
        "Negligence",
        "Indemnifications",
        "Confidentiality",
        "Lead Paint Disclosure",
        "Sublets"
    ]

    return questions, titles



# "Objectionable Conduct"
# Conditions for Early termination
# Possible tenant fees for anything
# Negligence (is the tenant liable for anything)
# Is the tenant being asked to indemnify the landlord for anything?
# Confidentiality agreement
# Lead Paint Disclosure
# Subletting
# Late payment fees/penalties
# Lease Termination reasons
# - when can tenant do it
# - when can landlord do it



    # 1. Does it say there is fixtures and furniture that come with the apartment? If so, flag these for the tenant so they can look for them when they move in and make sure they work on the day they move in.
    # 2. Are there any references to “objectionable conduct” in the lease? If so, flag the section for the tenant and check if it is defined. Also note what the consequences are for objectionable conduct.
    # 3. What are the reasons that allow the landlord to terminate the lease? List these in 6 words each.
    # 4. Can the tenant ever terminate the lease? When can the tenant terminate the lease?
    # - Look for statutory reasons that allow tenants to terminate and contrast
    # 5. Are there any instances where the landlord changes the tenant a fee for anything? Please list these instances and the sections of the lease.
    # 6. If there are any parts of the lease that make the tenant liable for negligence? If so, suggest asking the landlord to change this to say “gross negligence”
    # 7. Is the tenant being asked to indemnify the landlord for anything? Please list these reasons and flag the sections of the leas.e
    # - Contrasts against statutory circumstances where tenants are permitted to indemnify landlords
    # 8. Is the tenant required to take out renter’s insurance? If so, what section of the lease specifies this? How much is the insurance supposed to be for? Include a link to Lemonade.
    # 9. Is there a confidentiality requirement anywhere in the lease?
    
    # 10. Does the lease include a “lead paint disclosure”? If so, note the section where this is in the lease. Suggest asking the landlord to explain this.