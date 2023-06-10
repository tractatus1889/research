import api

def valid_extraction(extracted_text, full_text):
    valid_prompt = f"""
You are a very meticulous fact-checker. You will be provided with a FULL TEXT and a CLAIM and your task is to check whether the CLAIM follows from the FULL TEXT, and to give a reason why.

FULL TEXT: Softdisk, a computer company in Shreveport, Louisiana, hired Carmack to work on Softdisk G-S (an Apple IIGS publication), introducing him to John Romero and other future key members of id Software such as Adrian Carmack (not related). Later, Softdisk would place this team in charge of a new, but short-lived, bi-monthly game subscription product called Gamer's Edge for the IBM PC (DOS) platform. In 1990, while still at Softdisk, Carmack, Romero, and others created the first of the Commander Keen games, a series that was published by Apogee Software, under the shareware distribution model, from 1991 onwards.[10] Afterwards, Carmack left Softdisk to co-found id Software.[11]

Carmack has pioneered or popularized the use of many techniques in computer graphics, including "adaptive tile refresh" for Commander Keen,[12] ray casting for Hovertank 3D, Catacomb 3-D, and Wolfenstein 3D, binary space partitioning which Doom became the first game to use,[13] surface caching which he invented for Quake, Carmack's Reverse (formally known as z-fail stencil shadows) which he devised for Doom 3, and MegaTexture technology, first used in Enemy Territory: Quake Wars.[14] Quake 3 popularized the fast inverse square root algorithm.[15]

Carmack's engines have also been licensed for use in other influential first-person shooters such as Half-Life, Call of Duty and Medal of Honor. In 2007, when Carmack was on vacation with his wife, he ended up playing some games on his cellphone, and decided he was going to make a "good" mobile game.[16][17]

On August 7, 2013, Carmack joined Oculus VR as their CTO.[18] On November 22, 2013, he resigned from id Software to work full-time at Oculus VR.[2][19] Carmack's reason for leaving was that id's parent company ZeniMax Media did not want to support Oculus Rift.[20] Carmack's role at both companies later became central to a ZeniMax lawsuit against Oculus' parent company, Facebook, claiming that Oculus stole ZeniMax's virtual reality intellectual property.[21][22][23] The trial jury absolved Carmack of liability, though Oculus and other corporate officers were held liable for trademark, copyright, and contract violations.[24]
CLAIM: Carmack has worked on software for companies such as Softdisk, id Software, Nike, and Oculus.
QUESTION: Is the CLAIM justified by the text given in FULL TEXT?
ANSWER: NO.
REASON: The FULL TEXT does not mention anything about Carmack working for Nike.

FULL TEXT: Boygenius (stylized as boygenius)[1] is an American indie rock supergroup[2][3][4][1] formed in 2018 by Julien Baker, Phoebe Bridgers, and Lucy Dacus.[5][6] Their self-titled debut EP was written and recorded at Sound City Studios in Los Angeles.[7][8][9] On January 18, 2023, the band announced their debut studio album, The Record, which was released on March 31.[10]

Bridgers has called the formation of the group "kind of an accident," wherein each of the members were simply fans of each other's work and then became friends.[1] Both Dacus and Bridgers had opened for Baker on separate tours in 2016, and they all ran in similar circles as young up-and-coming performers navigating the indie scene.[11][12]
CLAIM: Phoebe Bridgers has opened for Julien Baker.
QUESTION: Is the CLAIM justified by the text given in FULL TEXT?
ANSWER: YES.
REASON: The sentence "Both Dacus and Bridgers had opened for Baker on separate tours in 2016, and they all ran in similar circles as young up-and-coming performers navigating the indie scene" says in particular that Phoebe Bridgers has opened for Julien Baker.

FULL TEXT: {full_text}
CLAIM: {extracted_text}
QUESTION: Is the CLAIM justified by the text given in FULL TEXT?
ANSWER: (Remember to respond with "YES." or "NO.")
"""
    response_json = api.get_response(valid_prompt)
    response = response_json["content"]
    assert "YES" in response or "NO" in response
    return "YES" in response
