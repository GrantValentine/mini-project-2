import random
import sys
import csv
import statistics

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

def matchDoctors(unmatchedDoctors, numProposals):
    for doctor in unmatchedDoctors:
        while doctor.nextProposal < len(doctor.hospitalRanking):
            hospital = doctor.hospitalRanking[doctor.nextProposal]
            doctor.nextProposal += 1
            numProposals = numProposals + 1
            if hospital.matchedDoctor == None:
                hospital.matchedDoctor = doctor
                doctor.matchedHospital = hospital
                break
            elif hospital.doctorRanking.index(doctor) < hospital.doctorRanking.index(hospital.matchedDoctor):
                hospital.matchedDoctor.matchedHospital = None
                hospital.matchedDoctor = doctor
                doctor.matchedHospital = hospital
                break
    return(numProposals)


def main():
    """
    This is the main funtion that will run DPDA for many iterations and for many values of n

    Inputs:
        All come from the command line so order is important
        startN: the number (n) of hospitals and doctors to run iterations on first
        endN: the number (n) of hospitals and doctors to end iterations on
        numRuns: the number of iterations to run for each value of n

    """
    startN = int(sys.argv[1])
    endN = int(sys.argv[2])
    stepN = int(sys.argv[3])
    numRuns = int(sys.argv[4])
    totalProposalsPern = []
    #print(startN, ", ", endN, ", ", numRuns)

    ## Run with various values of doctors and hospitals
    for nAmount in range(startN, endN+1, stepN):
        ## run many times to get averages
        tupleOfnAndProposals = (0,0)
        for run in range(numRuns):
            n = nAmount # number of hospitals and doctors
            numProposals = 0
            listOfHospitals = []
            listOfDoctors = []
            doctorMatchRankings = []
            hospitalMatchRankings = []
            for i in range(n):
                listOfHospitals.append(Hospital(i+1))
                listOfDoctors.append(Doctor(i+1))

            ## Generate random hospital rankings for each doctor 
            for doctor in listOfDoctors:
                doctor.hospitalRanking = random.sample(listOfHospitals,n)
            ## Generate random doctor rankings for each hospital 
            for hospital in listOfHospitals:
                hospital.doctorRanking = random.sample(listOfDoctors,n)

            ## Match unmatched doctors
            while getUnmatchedDoctor(listOfDoctors) != []:
                numProposals = matchDoctors(getUnmatchedDoctor(listOfDoctors), numProposals)
            
            ## Get average rankings of matches
            for doctor in listOfDoctors:
                doctorMatchRankings.append(doctor.hospitalRanking.index(doctor.matchedHospital))
            for hospital in listOfHospitals:
                hospitalMatchRankings.append(hospital.doctorRanking.index(hospital.matchedDoctor))

            averageDoctorMatch = statistics.mean(doctorMatchRankings)
            averageHospitalMatch = statistics.mean(hospitalMatchRankings)

            tupleOfnAndProposals = (n, numProposals, averageDoctorMatch, averageHospitalMatch)
            totalProposalsPern.append(tupleOfnAndProposals)

    ## Write to csv
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Number doctors and hospitals', 'Number of proposals', 'Average rank of match for doctors', 'Average rank of match for hospitals']) 
        writer.writerows(totalProposalsPern)

if __name__ == "__main__":
    main()
