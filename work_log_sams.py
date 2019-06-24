import datetime

class main:

    """[
        [days,
            tot_work,
            tot_plan,
            [start_time,],
            [end_time,],
            [comment,],
        ],
    ]"""

    log =[
            [20190624,
                0,
                0,
                [10,],
                [11,],
                ["Stadied a list as work_log.",],
            ],
        ]

    def add_rec(self,date,start,end,comment):
        """Used when adding a new record.
        parameters(date,start,end,domment)"""
        pass

if __name__ == "__main__":
    print(main.log[0][5][0])
