import win32com.client as win32
import pandas as pd
from pandas import ExcelWriter
import math

#wb_data = xlrd.open_workbook("C:/Users/Jayashree RAMAN/Documents/Tutorials and Notes/PersonalProjects/Python_RecommenderSystems/TrainingData.xlsx")
df = pd.read_excel('TrainingData.xlsx', sheet_name='Sheet1')

col_names=(df.columns)

customers = df['Customer Name']     #Get names of all customers
#print(customers)

custPrefDict = dict()
prefDict = dict()


size =(df.shape)       #Get the dimensions of the data set
rows = (size[0])-1
cols = (size[1]) - 1
#print(rows)

print(df)

for i in range(0, rows):
        prefDict={}
        #print(customers[i])
        for j in range (1, cols):
                #print(col_names[j])
                #print(df.at[i, col_names[j]])
                if (str(df.at[i, col_names[j]]) != 'nan'):
                
                        prefDict[col_names[j]] = df.at[i, col_names[j]]
                custPrefDict[customers[i]] = prefDict

#Code to check contents of the Customer preference data dictionary

for key in custPrefDict:
        #print(key)
        temp = custPrefDict[key]

        for k1 in temp:
                val = temp[k1]
                #print(str(key) + ':' + str(k1) + ':' + str(val))



def euclidean_similarity(P1, P2):
        common_ranked_items = [itm for itm in custPrefDict[P1] if itm in custPrefDict[P2]]
        #print(common_ranked_items)

        rankings = [(custPrefDict[P1][itm], custPrefDict[P2][itm]) for itm in common_ranked_items]
        distance = [pow(rank[0] - rank[1], 2) for rank in rankings]
        #print(distance)
        #print(1/(1+ sum(distance)))
        return 1/(1+ sum(distance))

def pearson_similarity(P1, P2):
        common_ranked_items =   [itm for itm in custPrefDict[P1] if itm in custPrefDict[P2]]
        no = len(common_ranked_items)
        s1 = sum(custPrefDict[P1][item] for item in common_ranked_items)
        s2 = sum(custPrefDict[P2][item] for item in common_ranked_items)

        ss1 = sum([pow(custPrefDict[P1][item], 2) for item in common_ranked_items])
        ss2 = sum([pow(custPrefDict[P2][item], 2) for item in common_ranked_items])

        ps = sum(custPrefDict[P1][item] * custPrefDict[P2][item] for item in common_ranked_items)

        num = no * ps - (s1*s2)

        den = math.sqrt((no*ss1 - math.pow(s1, 2)) * (no*ss2 - math.pow(s2,2)))

        return (num/den) if den !=0 else 0


def recommend(person, bound, similarity):
        scores = [(similarity(person, other), other) for other in custPrefDict if other != person]

        scores.sort()
        scores.reverse()
        scores = scores[0:bound]
        print(scores)


        recommendations = {}

        for sim, other in scores:
                ranked = custPrefDict[other]

        for itm in ranked:
                if itm not in custPrefDict[person]:
                        weight = sim * ranked[itm]

                        if itm in recommendations:
                                s, weights = recommendations[itm]
                                recommendations[itm] = (s + sim, weights + [weight])
                        else:
                                recommendations[itm] = (sim, [weight])
        for r in recommendations:
                sim, item = recommendations[r]
                recommendations[r] = sum(item)/sim

        return recommendations

print(recommend('Bhavna', 3, euclidean_similarity))
print(recommend('Bhavna', 3, pearson_similarity))
