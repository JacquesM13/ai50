        return_dict = {}
        N = len(corpus)
        
        inbound_dict = {}
        
        for key in corpus:
            return_dict[key] = 1/N
            
        for page in return_dict:
            for key, value in corpus.items():
                if page in value:
                    if page in inbound_dict:
                        inbound_dict[page].append(key)
                    else:
                        inbound_dict[page] = [key]
                
        for key in corpus:
            if len(corpus[key]) == 0:
                for page in corpus.keys():
                    corpus[key].add(page)
        
        notConverged = True
        
        while notConverged:
            
            return_dict_copy = return_dict.copy()
            
            for page in return_dict_copy:
                print("page : " + page)
                return_dict[page] = (1-damping_factor)/len(corpus)
                for value in inbound_dict[page]:
                    print("value: " + value)
                    increment = damping_factor*(return_dict_copy[value]/len(corpus[value]))
                    return_dict[page] += increment
                    
            for page in return_dict_copy:
                if return_dict_copy[page] - 0.001 < return_dict[page] < return_dict_copy[page] + 0.001:
                    notConverged = False
                else:
                    notConverged = True
            
            print(return_dict.values())
