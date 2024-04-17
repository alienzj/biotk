def convert_blast_json_to_dataframe(json_file):
    """Convert blast results of json format to Pandas dataframe

    Parameters:
        json_file: a string path of json file, like ~/blast.json

    Return:
        a Pandas dataframe object
    """

    import json
    import pandas as pd

    blast_dict = {
        "program": [],
        "version": [],
        "search_target": [],
        "params": [],
        
        "query_id": [],
        "query_title": [],
        "query_len": [],
        "stat": [],
        
        "hits_num": [],
        
        "hits_description_id": [],
        "hits_description_accession": [],
        "hits_description_title": [],
        "hits_description_taxid": [],
        "hits_description_sciname": [],
        
        "hits_len": [],
        
        "hits_hsps_num": [],
        "hits_hsps_bit_score": [],
        "hits_hsps_score": [],
        "hits_hsps_evalue": [],
        "hits_hsps_identity": [],
        "hits_hsps_query_from": [],
        "hits_hsps_query_to": [],
        "hits_hsps_query_strand": [],
        "hits_hsps_hit_from": [],
        "hits_hsps_hit_to": [],
        "hits_hsps_hit_strand": [],
        "hits_hsps_align_len": [],
        "hits_hsps_gaps": [],
        "hits_hsps_qseq": [],
        "hits_hsps_hseq": [],
        "hits_hsps_midline": []
    }

    with open(json_file, "rt") as ih:
        blast_json = json.load(ih)
        for res in blast_json["BlastOutput2"]:
            program = res["report"]["program"]
            version = res["report"]["version"]
            search_target = res["report"]["search_target"]
            params = res["report"]["search_target"]

            query_id = res["report"]["results"]["search"]["query_id"]
            query_title = res["report"]["results"]["search"]["query_title"]
            query_len = res["report"]["results"]["search"]["query_len"]
            stat = res["report"]["results"]["search"]["stat"]

            for hits in res["report"]["results"]["search"]["hits"]:
                blast_dict["program"].append(program)
                blast_dict["version"].append(version)
                blast_dict["search_target"].append(search_target)
                blast_dict["params"].append(params)
                
                blast_dict["query_id"].append(query_id)
                blast_dict["query_title"].append(query_title)
                blast_dict["query_len"].append(query_len)
                blast_dict["stat"].append(stat)

                
                blast_dict["hits_num"].append(hits["num"])
        
                blast_dict["hits_description_id"].append(hits["description"][0]["id"])
                blast_dict["hits_description_accession"].append(hits["description"][0]["accession"])
                blast_dict["hits_description_title"].append(hits["description"][0]["title"])
                blast_dict["hits_description_taxid"].append(hits["description"][0]["taxid"])
                blast_dict["hits_description_sciname"].append(hits["description"][0]["sciname"])
        
                blast_dict["hits_len"].append(hits["len"])
        
                blast_dict["hits_hsps_num"].append(hits["hsps"][0]["num"])
                blast_dict["hits_hsps_bit_score"].append(hits["hsps"][0]["bit_score"])
                blast_dict["hits_hsps_score"].append(hits["hsps"][0]["score"])
                blast_dict["hits_hsps_evalue"].append(hits["hsps"][0]["evalue"])
                blast_dict["hits_hsps_identity"].append(hits["hsps"][0]["identity"])
                blast_dict["hits_hsps_query_from"].append(hits["hsps"][0]["query_from"])
                blast_dict["hits_hsps_query_to"].append(hits["hsps"][0]["query_to"])
                blast_dict["hits_hsps_query_strand"].append(hits["hsps"][0]["query_strand"])
                blast_dict["hits_hsps_hit_from"].append(hits["hsps"][0]["hit_from"])
                blast_dict["hits_hsps_hit_to"].append(hits["hsps"][0]["hit_to"])
                blast_dict["hits_hsps_hit_strand"].append(hits["hsps"][0]["hit_strand"])
                blast_dict["hits_hsps_align_len"].append(hits["hsps"][0]["align_len"])
                blast_dict["hits_hsps_gaps"].append(hits["hsps"][0]["gaps"])
                blast_dict["hits_hsps_qseq"].append(hits["hsps"][0]["qseq"])
                blast_dict["hits_hsps_hseq"].append(hits["hsps"][0]["hseq"])
                blast_dict["hits_hsps_midline"].append(hits["hsps"][0]["midline"])
                
    blast_df = pd.DataFrame(blast_dict)
    blast_df["hits_hsps_percent_identity"] = blast_df["hits_hsps_identity"] / blast_df["hits_hsps_align_len"]

    return blast_df