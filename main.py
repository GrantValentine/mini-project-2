import random

class Doctor:
    def __init__(self, docID):
        self.docID = docID
        self.hospitalRanking = []
        self.matchedHospital = None
        self.nextProposal = 0

class Hospital:
    def __init__(self, hospitalID):
        self.hospitalID = hospitalID
        self.doctorRanking = []
        self.matchedDoctor = None

def getUnmatchedDoctor(listOfDoctors):
    """
    This function returns a list of doctors that are not matched
    """
    unmatchedDoctors = []
    for doctor in listOfDoctors:
        if doctor.matchedHospital == None:
            unmatchedDoctors.append(doctor)
    return unmatchedDoctors

def matchDoctors(unmatchedDoctors):
    for doctor in unmatchedDoctors:
        while doctor.nextProposal < len(doctor.hospitalRanking):
            hospital = doctor.hospitalRanking[doctor.nextProposal]
            doctor.nextProposal += 1
            if hospital.matchedDoctor == None:
                hospital.matchedDoctor = doctor
                doctor.matchedHospital = hospital
                print(doctor.docID," matched with ", hospital.hospitalID, " through default")
                break
            elif hospital.doctorRanking.index(doctor) < hospital.doctorRanking.index(hospital.matchedDoctor):
                hospital.matchedDoctor.matchedHospital = None
                hospital.matchedDoctor = doctor
                doctor.matchedHospital = hospital
                print(doctor.docID," matched with ", hospital.hospitalID, " through higher rank")
                break


def main():
    ## Eventually replace by input
    n = 3 # number of hospitals and doctors
    listOfHospitals = []
    listOfDoctors = []
    for i in range(n):
        listOfHospitals.append(Hospital(i+1))
        listOfDoctors.append(Doctor(i+1))

    ## Generate random hospital rankings for each doctor or use the input from user
    for doctor in listOfDoctors:
        doctor.hospitalRanking = random.sample(listOfHospitals,n)
        print("Doctor ", doctor.docID, "'s rankings")
        for hospital in doctor.hospitalRanking:
           print(hospital.hospitalID)

    ## Generate random doctor rankings for each hospital or use the input from user
    for hospital in listOfHospitals:
        hospital.doctorRanking = random.sample(listOfDoctors,n)
        print("Hospital ", hospital.hospitalID, "'s rankings" "")
        for doctor in hospital.doctorRanking:
           print(doctor.docID)
    ## Match unmatched doctors
    while getUnmatchedDoctor(listOfDoctors) != []:
        matchDoctors(getUnmatchedDoctor(listOfDoctors))


    ## Print the final matching list
    for doctor in listOfDoctors:
        print("doctor ", doctor.docID, " matched with hospital ", doctor.matchedHospital.hospitalID)
        
    for hospital in listOfHospitals:
        ##print("doctor ", hospital.matchedDoctor.docID, " matched with hospital ", hospital.hospitalID)
        pass

if __name__ == "__main__":
    main()
