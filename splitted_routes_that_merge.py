def splittedRoutesThatMerge(route1, route2):
    hasSplitted = False
    hasMerged = False
    if (len(route1) > len(route2)):
        route1_tmp = route1
        route1 = route2
        route2 = route1_tmp

    for i in range(0, len(route1)):
        if (route1[0] == route2[0]): 
            if (hasSplitted == False and hasMerged == False and route1[i] != route2[i]):
                hasSplitted = True
                splitNode = i

            elif (hasMerged == False and hasSplitted):
                for j in range(splitNode, len(route2)):
                    if (route1[i] == route2[j]):
                        hasMerged = True
                        mergeNode1 = i
                        mergeNode2 = j
                        



            elif (hasMerged and hasSplitted):
                for j in range(max(mergeNode1,mergeNode2), len(route1)):
                    if (mergeNode1 > mergeNode2):
                        if (route1[j] != route2[mergeNode2-mergeNode1+j]):
                            return True
                              
                    elif (mergeNode2 > mergeNode1):
                        if (route1[mergeNode1-mergeNode2+j] != route2[j]):
                            return True
                            
                    elif (route1[j] != route2[j]):
                     
                        return True
        else:
            return False

def getSplittedRoutesThatMerge(routes):
    splitted_routes_that_merge = []
    for i in range(0, len(routes)-1):
        for j in range(i+1, len(routes)):
            if (splittedRoutesThatMerge(routes[i], routes[j])):
                splitted_routes_that_merge.append((i, j))

                #splitted_routes_that_merge = splitted_routes_that_merge + 1
                

    return splitted_routes_that_merge
                


