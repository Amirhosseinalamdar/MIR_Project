
from typing import List
import math
from bs4 import BeautifulSoup
import requests
import wandb
import json

class Evaluation:

    def __init__(self, name: str):
            self.name = name

    def calculate_precision(self, actual: List[str], predicted: List[str]) -> float:
        """
        Calculates the precision of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The precision of the predicted results
        """
        precision = len(set(predicted).intersection(set(actual))) / len(predicted)
        # TODO: Calculate precision here
        
        return precision
    
    def calculate_recall(self, actual: List[str], predicted: List[str]) -> float:
        """
        Calculates the recall of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The recall of the predicted results
        """
        if len(actual) == 0:
            print('imdb didn\'t retrieved good enough!!')
            return None
        recall = len(set(predicted).intersection(set(actual))) / len(actual)
        # TODO: Calculate recall here
        return recall
    
    def calculate_F1(self, actual: List[str], predicted: List[str]) -> float:
        """
        Calculates the F1 score of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The F1 score of the predicted results    
        """
        r = self.calculate_recall(actual, predicted)
        p = self.calculate_precision(actual, predicted)
        if p is None or r is None or p + r == 0.0:
            return None
        f1 = 2*p*r / (p + r)
        # TODO: Calculate F1 here

        return f1
    
    def calculate_AP(self, actual: List[str], predicted: List[str]) -> float:
        """
        Calculates the Mean Average Precision of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The Average Precision of the predicted results
        """
        AP = 0.0
        cnt = 0
        for i, doc_id in enumerate(predicted):
            if doc_id in actual:
                AP += self.calculate_precision(actual, predicted[:i+1])
                cnt += 1
        
        if cnt == 0:
            AP = 0
        else:
            AP /= cnt

        # TODO: Calculate AP here

        return AP
    
    def calculate_MAP(self, actual: List[List[str]], predicted: List[List[str]]) -> float:
        """
        Calculates the Mean Average Precision of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The Mean Average Precision of the predicted results
        """
        MAP = 0.0
        for i, rel_docs in enumerate(predicted):
            MAP += self.calculate_AP(actual[i], rel_docs)
        
        assert len(actual) == len(predicted), "The actual results not the same as predicted"
        MAP /= len(actual)
        # TODO: Calculate MAP here

        return MAP
    
    def calculate_DCG(self, actual: List[str], predicted: List[str]) -> float:
        """
        Calculates the Normalized Discounted Cumulative Gain (NDCG) of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The DCG of the predicted results
        """
        DCG = 0.0
        for i, pred in enumerate(predicted):
            score = self.get_rate_score(actual, pred)
            DCG += score / math.log2(i + 2)
        # TODO: Calculate DCG here

        return DCG
    def get_rate_score(self, actual, doc_id):
        if doc_id not in actual:
            return 0
        
        index = actual.index(doc_id)
        return 1 - index / len(actual)



    def calculate_ideal_DCG(self, actual, predicted):
        res = 0.0
        lst = []
        for i, pred in enumerate(predicted):
            lst.append(self.get_rate_score(actual, pred))
        lst = sorted(lst, reverse = True)

        for i, el in enumerate(lst):
            res += el / math.log2(i + 2)
        
        return res

    def calculate_NDCG(self, actual: List[List[str]], predicted: List[List[str]]) -> float:
        """
        Calculates the Normalized Discounted Cumulative Gain (NDCG) of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The NDCG of the predicted results
        """
        if len(actual) == 0:
            print('imdb didn\'t retrieved good enough!!')
            return None
        NDCG = 0.0
        for pred, real in zip(predicted, actual):
            ideal = self.calculate_ideal_DCG(real, pred)
            if ideal == 0:
                print('conflict!!, returned 0 because mine is better than imdb')
                continue
            NDCG += self.calculate_DCG(real, pred) / ideal
        NDCG /= len(actual)
        # TODO: Calculate NDCG here

        return NDCG
    
    def calculate_RR(self, actual: List[str], predicted: List[str]) -> float:
        """
        Calculates the Mean Reciprocal Rank of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The Reciprocal Rank of the predicted results
        """
        RR = 0.0
        for i, pred in enumerate(predicted):
            if pred in actual:
                RR = 1 / (i + 1)
                break
        # TODO: Calculate MRR here

        return RR
    
    def calculate_MRR(self, actual: List[List[str]], predicted: List[List[str]]) -> float:
        """
        Calculates the Mean Reciprocal Rank of the predicted results

        Parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results

        Returns
        -------
        float
            The MRR of the predicted results
        """
        MRR = 0.0

        # TODO: Calculate MRR here
        for pred, real in zip(predicted, actual):
            MRR += self.calculate_RR(pred, real)
        
        MRR /= len(predicted)

        return MRR
    

    def print_evaluation(self, precision, recall, f1, ap, dcg, rr):
        """
        Prints the evaluation metrics

        parameters
        ----------
        precision : float
            The precision of the predicted results
        recall : float
            The recall of the predicted results
        f1 : float
            The F1 score of the predicted results
        ap : float
            The Average Precision of the predicted results
        map : float
            The Mean Average Precision of the predicted results
        dcg: float
            The Discounted Cumulative Gain of the predicted results
        ndcg : float
            The Normalized Discounted Cumulative Gain of the predicted results
        rr: float
            The Reciprocal Rank of the predicted results
        mrr : float
            The Mean Reciprocal Rank of the predicted results
            
        """

        print(f"name = {self.name}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1 Score: {f1}")
        print(f"Average Precision: {ap}")
        print(f"Discounted Cumulative Gain: {dcg}")
        print(f"Reciprocal Rank: {rr}")
        print('==========================================')
      

    def log_evaluation(self, precision, recall, f1, ap, dcg, rr):
        """
        Use Wandb to log the evaluation metrics
      
        parameters
        ----------
        precision : float
            The precision of the predicted results
        recall : float
            The recall of the predicted results
        f1 : float
            The F1 score of the predicted results
        ap : float
            The Average Precision of the predicted results
        map : float
            The Mean Average Precision of the predicted results
        dcg: float
            The Discounted Cumulative Gain of the predicted results
        ndcg : float
            The Normalized Discounted Cumulative Gain of the predicted results
        rr: float
            The Reciprocal Rank of the predicted results
        mrr : float
            The Mean Reciprocal Rank of the predicted results
            
        """
        
        
        wandb.init(project="evaluation_logs", name=self.name)

        wandb.log({
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
            "Average Precision": ap,
            # "Mean Average Precision": map,
            "Discounted Cumulative Gain": dcg,
            # "Normalized Discounted Cumulative Gain": ndcg,
            "Reciprocal Rank": rr,
            # "Mean Reciprocal Rank": mrr
        })

        wandb.finish()
    
    def calculate_evaluation(self, actual: List[List[str]], predicted: List[List[str]]):
        """
        call all functions to calculate evaluation metrics

        parameters
        ----------
        actual : List[List[str]]
            The actual results
        predicted : List[List[str]]
            The predicted results
            
        """

        for real, pred in zip(actual, predicted):
            precision = self.calculate_precision(real, pred)
            recall = self.calculate_recall(real, pred)
            print(real, pred)
            f1 = self.calculate_F1(real, pred)
            ap = self.calculate_AP(real, pred)
            dcg = self.calculate_DCG(real, pred)
            rr = self.calculate_RR(real, pred)
            self.print_evaluation(precision, recall, f1, ap, dcg, rr)
            # self.log_evaluation(precision, recall, f1, ap, dcg, rr)


        map_score = self.calculate_MAP(actual, predicted)
        ndcg = self.calculate_NDCG(actual, predicted)
        mrr = self.calculate_MRR(actual, predicted)

        print(f"Mean Average Precision: {map_score}")
        print(f"Normalized Discounted Cumulative Gain: {ndcg}")
        print(f"Mean Reciprocal Rank: {mrr}")



with open('./utility/prep_eval_data.json', "r") as json_file:
    eval_data = json.load(json_file)

with open('./utility/search_data.json', "r") as json_file:
    predicted_data = json.load(json_file)


actual = []
for key in eval_data:
    actual.append(eval_data[key])

predicted = []
for key in predicted_data:
    predicted.append(predicted_data[key])

evaluator = Evaluation('aaaaaaaaaah')

evaluator.calculate_evaluation(actual, predicted)
