from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
result = client['testDB']['penna'].aggregate([
    {
        '$group': {
            '_id': '$Timestamp', 
            'totalvotes': {
                '$sum': '$totalvotes'
            }
        }
    }, {
        '$sort': {
            '_id': 1
        }
    }, {
        '$group': {
            '_id': None, 
            'all': {
                '$push': '$$ROOT'
            }
        }
    }, {
        '$addFields': {
            'allWithIndex': {
                '$zip': {
                    'inputs': [
                        '$all', {
                            '$range': [
                                0, {
                                    '$size': '$all'
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }, {
        '$project': {
            'pairs': {
                '$map': {
                    'input': '$allWithIndex', 
                    'in': {
                        'current': {
                            '$arrayElemAt': [
                                '$$this', 0
                            ]
                        }, 
                        'prev': {
                            '$arrayElemAt': [
                                '$all', {
                                    '$max': [
                                        0, {
                                            '$subtract': [
                                                {
                                                    '$arrayElemAt': [
                                                        '$$this', 1
                                                    ]
                                                }, 1
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }
        }
    }, {
        '$unwind': {
            'path': '$pairs'
        }
    }, {
        '$group': {
            '_id': '$pairs.current._id', 
            'TotIncrement': {
                '$sum': {
                    '$subtract': [
                        '$pairs.current.totalvotes', '$pairs.prev.totalvotes'
                    ]
                }
            }
        }
    }, {
        '$sort': {
            'TotIncrement': -1
        }
    }, {
        '$limit': 1
    }
])
for i in result:
    print(i)