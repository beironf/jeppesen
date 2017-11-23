def splittedRoutesThatMerge(route1, route2):
    hasSplitted = False
    hasMerged = False
    if (len(route1) >= len(route2)):
        for i in range(0, len(route1)):
            if (route1[0] == route2[0]): 
                if (hasSplitted == False and hasMerged == False and route1[i] != route2[i]):
                    hasSplitted = True
                    splitNode = i

                elif (hasMerged == False and hasSplitted == True):
                    for j in range(splitNode, len(route2)):
                        if (route1[i] == route2[j]):
                            hasMerged = True
                            mergeNode1 = i
                            mergeNode2 = j
                            break
                        

                elif (hasMerged == True and hasSplitted == True):
                    for j in range(0, min(len(route2)-mergeNode2, len(route1)-mergeNode1)):
                            if (route1[mergeNode1+j] != route2[mergeNode2+j]):
                                return [[route1[0], route1[mergeNode1-1], route1[mergeNode1], route2[mergeNode2+j]], [route2[0], route2[mergeNode2-1], route2[mergeNode2], route1[mergeNode1+j]]]
            else:
                return []

def getSplittedRoutesThatMerge(routes):
    forbidden_seqs = []
    for i in range(0, len(routes)):
        for j in range(0, len(routes)):
            if i != j and splittedRoutesThatMerge(routes[i], routes[j]):
                forbidden_seqs.extend(splittedRoutesThatMerge(routes[i], routes[j]))

                #splitted_routes_that_merge = splitted_routes_that_merge + 1

    #forbidden_seqs = [x for x in forbidden_seqs if x]                

    return forbidden_seqs
                


