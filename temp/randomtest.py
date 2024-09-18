import random
import string

def main():
    randomData = randomNameGenerator()
    rLN = randomData[0]
    rFN = randomData[1]
    rEm = randomData[2]
    rTp = randomData[3]
    print(f"Random Name: {rLN} {rFN}")
    print(f"Random Email: {rEm}")
    print(f"Random Telephone: {rTp}")
    
def randomNameGenerator():
    lastnameLength = 8
    firstnameLength = 5
    emailHostLength = 8
    emailTLD = ".invalid"
    telephoneLength = 10

    randTelephone = str(''.join(random.choices(string.digits, k=telephoneLength)))
    randFirstname = str(''.join(random.choices(string.ascii_lowercase, k=firstnameLength)))
    randLastname = str(''.join(random.choices(string.ascii_lowercase, k=lastnameLength)))
    randEmailHost = str(''.join(random.choices(string.ascii_lowercase, k=emailHostLength)))
    randEmail = str(randFirstname) + "@" + str(randEmailHost) + str(emailTLD)

    return randLastname, randFirstname, randEmail, randTelephone

if __name__ == "__main__":
    main()