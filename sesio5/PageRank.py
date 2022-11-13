#!/usr/bin/python

import sys
import time


class Edge:
    def __init__(self, origin=None):
        self.origin = origin  # write appropriate value
        self.weight = 1.0  # write appropriate value

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)

    # write rest of code that you need for this class


class Airport:
    def __init__(self, iden=None, name=None, indx=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0.0  # write appropriate value
        self.indx = indx

    def addInEdge(self, inAirport):
        if inAirport in self.routeHash:
            edge = self.routeHash[inAirport]
            edge.weight += 1.0
        else:
            edge = Edge(inAirport)
            self.routeHash[inAirport] = edge
            self.routes.append(edge)

    def __repr__(self):
        return f"{self.code}\t{self.pageIndex}\t{self.name}"


edgeList = []  # list of Edge
edgeHash = dict()  # hash of edge to ease the match
airportList = []  # list of Airport
airportHash = dict()  # hash key IATA code -> Airport
pageRank = []  # list of page rank


def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r")
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5:
                raise Exception('not an IATA code')
            a.name = temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code = temp[4][1:-1]
            a.indx = cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print(f"There were {cont} Airports with IATA code")


def readRoutes(fd):
    print("Reading Routes file from {0}".format(fd))
    # write your code
    routesTxt = open(fd, "r")
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')
            origin = temp[2]
            destination = temp[4]
            if not (origin in airportHash) or not (destination in airportHash):
                raise Exception('The airport does not exist')
            airportHash[destination].addInEdge(origin)
            airportHash[origin].outweight += 1.0
        except Exception as inst:
            pass
        else:
            cont += 1
    routesTxt.close()
    print(f"There were {cont} Edges with IATA code")


def computePageRanks():
    L = 0.85
    condition = 10**(-12)
    n = len(airportHash)
    P = [1 / n] * n
    stop = False
    aux1 = (1.0 - L) / n
    aux2 = 1 / n

    # Calculating the disconnected nodes in the page rank (In pagerank.pdf, Important points number 3)
    listDisconected = []
    for element in airportList:
        if element.outweight == 0.0:
            listDisconected.append(element)

    disconectedNodes = len(listDisconected)
    totalDisconected = L / float(n) * disconectedNodes

    iteration = 0
    while not stop:
        Q = [0.0] * n
        for i in range(n):
            airport = airportList[i]
            suma = 0
            for air, edge in airport.routeHash.items():
                weight = edge.weight  # w(j,i)
                out = airportHash[air].outweight  # out(j)
                suma += P[airportHash[air].indx] * weight / out  # sum { P[j] * w(j,i) / out(j) : there is an edge (j,i) in G }
            Q[i] = L * suma + aux1 + totalDisconected * aux2

        aux2 = aux1 + aux2 * totalDisconected
      
        stop = checkCondition(P, Q, condition)
#        if iteration == 100: stop = True
        P = Q
        # Does P sum 1 ?
        print("SUM:" + str(sum(P)))
        iteration += 1

    global pageRank
    pageRank = P
    return iteration


def checkCondition(P, Q, cond):
# We create tuples of (first element of P, first element of Q), (second element of P, second element of Q)
# and we substract them to check if it complies with the stopping condition
    for x, y in zip(P,Q):
        if (abs(x-y) > cond):
            return False
    return True

def outputPageRanks():
    # List where we will save the tuple (airport_name, page_rank)
    mylist = []
    j = 0
    for i in airportHash:
        element = (airportHash[i].name, pageRank[j])
        mylist.append(element)
        j += 1
    # Sort by decreasing page rank    
    mylist.sort(key=lambda x: x[1], reverse=True)

    print(" ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ ( Page rank, Airport name) ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ ")

    for air, pageR in mylist:
        print('(' + str(pageR) + ", " + str(air) + ')')


def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2 - time1)


if __name__ == "__main__":
    sys.exit(main())
