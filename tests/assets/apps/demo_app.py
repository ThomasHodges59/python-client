import base64
import io
from typing import Any, Dict

from pydantic import BaseModel

from steamship.app import App, Response, create_handler, get, post
from steamship.base import Client
from steamship.base.mime_types import MimeTypes


class TestObj(BaseModel):
    name: str


# noinspection PyPep8
PALM_TREE_BASE_64 = "iVBORw0KGgoAAAANSUhEUgAAADgAAABWCAYAAACaeFU0AAAMbWlDQ1BJQ0MgUHJvZmlsZQAASImVVwdYU8kWnluSkJDQAghICb0jUgNICaEFkF4EGyEJJJQYE4KKvSwquHYRxYquiii2lWYBsSuLYu+LBRVlXdTFhsqbkICu+8r3zvfNvX/OnPlPuTO59wCg+YErkeShWgDkiwukCeHBjDFp6QzSU4AAKqADHeDK5ckkrLi4aABl8P53eXcDWkO56qzg+uf8fxUdvkDGAwAZB3EmX8bLh7gZAHwDTyItAICo0FtOKZAo8ByIdaUwQIhXK3C2Eu9S4EwlPjpgk5TAhvgyAGpULleaDYDGPahnFPKyIY/GZ4hdxXyRGABNJ4gDeEIuH2JF7E75+ZMUuBxiO2gvgRjGA5iZ33Fm/40/c4ify80ewsq8BkQtRCST5HGn/Z+l+d+Snycf9GEDB1UojUhQ5A9reCt3UpQCUyHuFmfGxCpqDfEHEV9ZdwBQilAekay0R415MjasH9CH2JXPDYmC2BjiMHFeTLRKn5klCuNADHcLOlVUwEmC2ADiRQJZaKLKZot0UoLKF1qbJWWzVPpzXOmAX4WvB/LcZJaK/41QwFHxYxpFwqRUiCkQWxWKUmIg1oDYRZabGKWyGVUkZMcM2kjlCYr4rSBOEIjDg5X8WGGWNCxBZV+SLxvMF9siFHFiVPhggTApQlkf7BSPOxA/zAW7LBCzkgd5BLIx0YO58AUhocrcsecCcXKiiueDpCA4QbkWp0jy4lT2uIUgL1yht4DYQ1aYqFqLpxTAzankx7MkBXFJyjjxohxuZJwyHnw5iAZsEAIYQA5HJpgEcoCorbuuG/5SzoQBLpCCbCAAzirN4IrUgRkxvCaCIvAHRAIgG1oXPDArAIVQ/2VIq7w6g6yB2cKBFbngKcT5IArkwd/ygVXiIW8p4AnUiP7hnQsHD8abB4di/t/rB7XfNCyoiVZp5IMeGZqDlsRQYggxghhGtMeN8ADcD4+G1yA43HAm7jOYxzd7wlNCO+ER4Tqhg3B7omie9IcoR4MOyB+mqkXm97XAbSCnJx6M+0N2yIzr40bAGfeAflh4IPTsCbVsVdyKqjB+4P5bBt89DZUd2ZWMkoeRg8h2P67UcNDwHGJR1Pr7+ihjzRyqN3to5kf/7O+qz4f3qB8tsUXYIewsdgI7jx3F6gADa8LqsVbsmAIP7a4nA7tr0FvCQDy5kEf0D39clU9FJWWu1a5drp+VcwWCqQWKg8eeJJkmFWULCxgs+HYQMDhinosTw83VzQ0AxbtG+ff1Nn7gHYLot37Tzf8dAP+m/v7+I990kU0AHPCGx7/hm86OCYC2OgDnGnhyaaFShysuBPgvoQlPmiEwBZbADubjBryAHwgCoSASxIIkkAYmwCoL4T6XgilgBpgLikEpWA7WgPVgM9gGdoG94CCoA0fBCXAGXASXwXVwF+6eTvAS9IB3oA9BEBJCQ+iIIWKGWCOOiBvCRAKQUCQaSUDSkAwkGxEjcmQGMh8pRVYi65GtSBVyAGlATiDnkXbkNvIQ6ULeIJ9QDKWiuqgJaoOOQJkoC41Ck9DxaDY6GS1CF6BL0XK0Et2D1qIn0IvodbQDfYn2YgBTx/Qxc8wZY2JsLBZLx7IwKTYLK8HKsEqsBmuEz/kq1oF1Yx9xIk7HGbgz3MEReDLOwyfjs/Al+Hp8F16Ln8Kv4g/xHvwrgUYwJjgSfAkcwhhCNmEKoZhQRthBOEw4Dc9SJ+EdkUjUJ9oSveFZTCPmEKcTlxA3EvcRm4ntxMfEXhKJZEhyJPmTYklcUgGpmLSOtIfURLpC6iR9UFNXM1NzUwtTS1cTq81TK1PbrXZc7YraM7U+shbZmuxLjiXzydPIy8jbyY3kS+ROch9Fm2JL8ackUXIocynllBrKaco9ylt1dXULdR/1eHWR+hz1cvX96ufUH6p/pOpQHahs6jiqnLqUupPaTL1NfUuj0WxoQbR0WgFtKa2KdpL2gPZBg67hosHR4GvM1qjQqNW4ovFKk6xprcnSnKBZpFmmeUjzkma3FlnLRoutxdWapVWh1aB1U6tXm649UjtWO197ifZu7fPaz3VIOjY6oTp8nQU623RO6jymY3RLOpvOo8+nb6efpnfqEnVtdTm6Obqlunt123R79HT0PPRS9KbqVegd0+vQx/Rt9Dn6efrL9A/q39D/NMxkGGuYYNjiYTXDrgx7bzDcIMhAYFBisM/gusEnQ4ZhqGGu4QrDOsP7RriRg1G80RSjTUanjbqH6w73G84bXjL84PA7xqixg3GC8XTjbcatxr0mpibhJhKTdSYnTbpN9U2DTHNMV5seN+0yo5sFmInMVps1mb1g6DFYjDxGOeMUo8fc2DzCXG6+1bzNvM/C1iLZYp7FPov7lhRLpmWW5WrLFsseKzOr0VYzrKqt7liTrZnWQuu11met39vY2qTaLLSps3lua2DLsS2yrba9Z0ezC7SbbFdpd82eaM+0z7XfaH/ZAXXwdBA6VDhcckQdvRxFjhsd250ITj5OYqdKp5vOVGeWc6FztfNDF32XaJd5LnUur0ZYjUgfsWLE2RFfXT1d81y3u94dqTMycuS8kY0j37g5uPHcKtyuudPcw9xnu9e7v/Zw9BB4bPK45Un3HO250LPF84uXt5fUq8ary9vKO8N7g/dNpi4zjrmEec6H4BPsM9vnqM9HXy/fAt+Dvn/6Ofvl+u32ez7KdpRg1PZRj/0t/Ln+W/07AhgBGQFbAjoCzQO5gZWBj4Isg/hBO4KesexZOaw9rFfBrsHS4MPB79m+7Jns5hAsJDykJKQtVCc0OXR96IMwi7DssOqwnnDP8OnhzRGEiKiIFRE3OSYcHqeK0xPpHTkz8lQUNSoxan3Uo2iHaGl042h0dOToVaPvxVjHiGPqYkEsJ3ZV7P0427jJcUfiifFx8RXxTxNGJsxIOJtIT5yYuDvxXVJw0rKku8l2yfLklhTNlHEpVSnvU0NSV6Z2jBkxZuaYi2lGaaK0+nRSekr6jvTesaFj14ztHOc5rnjcjfG246eOPz/BaELehGMTNSdyJx7KIGSkZuzO+MyN5VZyezM5mRsye3hs3lreS34QfzW/S+AvWCl4luWftTLrebZ/9qrsLmGgsEzYLWKL1ote50TkbM55nxubuzO3Py81b1++Wn5GfoNYR5wrPjXJdNLUSe0SR0mxpGOy7+Q1k3ukUdIdMkQ2XlZfoAs/6lvldvKf5A8LAworCj9MSZlyaKr2VPHU1mkO0xZPe1YUVvTLdHw6b3rLDPMZc2c8nMmauXUWMitzVstsy9kLZnfOCZ+zay5lbu7c3+a5zls576/5qfMbF5gsmLPg8U/hP1UXaxRLi28u9Fu4eRG+SLSobbH74nWLv5bwSy6UupaWlX5ewlty4eeRP5f/3L80a2nbMq9lm5YTl4uX31gRuGLXSu2VRSsfrxq9qnY1Y3XJ6r/WTFxzvsyjbPNaylr52o7y6PL6dVbrlq/7vF64/npFcMW+DcYbFm94v5G/8cqmoE01m002l27+tEW05dbW8K21lTaVZduI2wq3Pd2esv3sL8xfqnYY7Sjd8WWneGfHroRdp6q8q6p2G+9eVo1Wy6u79ozbc3lvyN76Guearfv095XuB/vl+18cyDhw42DUwZZDzEM1v1r/uuEw/XBJLVI7rbanTljXUZ9W394Q2dDS6Nd4+IjLkZ1HzY9WHNM7tuw45fiC4/1NRU29zZLm7hPZJx63TGy5e3LMyWun4k+1nY46fe5M2JmTZ1lnm875nzt63vd8wwXmhbqLXhdrWz1bD//m+dvhNq+22kvel+ov+1xubB/VfvxK4JUTV0OunrnGuXbxesz19hvJN27dHHez4xb/1vPbebdf3ym803d3zj3CvZL7WvfLHhg/qPzd/vd9HV4dxx6GPGx9lPjo7mPe45dPZE8+dy54Snta9szsWdVzt+dHu8K6Lr8Y+6LzpeRlX3fxH9p/bHhl9+rXP4P+bO0Z09P5Wvq6/82St4Zvd/7l8VdLb1zvg3f57/rel3ww/LDrI/Pj2U+pn571TflM+lz+xf5L49eor/f68/v7JVwpd+BTAIMDzcoC4M1OAGhpANBh30YZq+wFBwRR9q8DCPwnrOwXB8QLgBr4/R7fDb9ubgKwfztsvyC/JuxV42gAJPkA1N19aKhEluXupuSiwj6F8KC//y3s2UirAPiyvL+/r7K//8s2GCzsHZvFyh5UIUTYM2yJ+5KZnwn+jSj70+9y/PEOFBF4gB/v/wLoupDSqduEDAAAAJZlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAIdpAAQAAAABAAAAWgAAAAAAAACQAAAAAQAAAJAAAAABAAOShgAHAAAAEgAAAISgAgAEAAAAAQAAADigAwAEAAAAAQAAAFYAAAAAQVNDSUkAAABTY3JlZW5zaG90mGCALAAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAtdpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIj4KICAgICAgICAgPGV4aWY6UGl4ZWxYRGltZW5zaW9uPjQ5NDwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlVzZXJDb21tZW50PlNjcmVlbnNob3Q8L2V4aWY6VXNlckNvbW1lbnQ+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj43NTY8L2V4aWY6UGl4ZWxZRGltZW5zaW9uPgogICAgICAgICA8dGlmZjpSZXNvbHV0aW9uVW5pdD4yPC90aWZmOlJlc29sdXRpb25Vbml0PgogICAgICAgICA8dGlmZjpZUmVzb2x1dGlvbj4xNDQ8L3RpZmY6WVJlc29sdXRpb24+CiAgICAgICAgIDx0aWZmOlhSZXNvbHV0aW9uPjE0NDwvdGlmZjpYUmVzb2x1dGlvbj4KICAgICAgICAgPHRpZmY6T3JpZW50YXRpb24+MTwvdGlmZjpPcmllbnRhdGlvbj4KICAgICAgPC9yZGY6RGVzY3JpcHRpb24+CiAgIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CjxwNDEAADD1SURBVHgBTZxXrKTnfd6fmfmmt9PP2dP3bOEWckmxqJFUVGxJcUtsywYcOIEROEGQduEgN4EvhAC5yU2M3NiAkWIlF4Ec24BluciKTFkSRUkkl2LRLrdyy+l1ep/J73lnV9bszk77vvd7//35l29jf/+3vzMaDmMajQZSLKbhaMR78eRVvPqPv/B7f/8T342G4+/Db+HIOAcMNRwM1WXNZCzBTzEp3uNcr+0j+czTn8drD8Oa4TvOi4UlErxy3KjLcawRY28/foyvyabH34w4gcd4j17bD179lmtEMYiKs+owxom8j5kKn+vP3pEP5HtWGL/nJD6Mv+JAvg2f5Y1ooH68r3wsrbWJQ90/LmkwzCoR62nAebH4eDNhofGJLGWKBiZZQ4iK8xzFR+r3+uyLz0k+BwGMLxPO9T4TXI81xrx/tG9vhYdpGhMYZz1fNPHo4izuH8OTI3yxGMSPT+C9v3v0e1jg0fF+733GEwOkl5WScZ1b+6FOz1xXbdBXIp5jQ2bKY6rCLryT8PTLKBYplRzpuNvUxemrenblSF00wOeYMfEE+/AagUnjPfn94/2F9/5sHrJeoJ5XH8GXbJwFeOGjiXpEXDhh/DkQ6QMeETU+zlT5O6uU10wrFU+qgqrVKrOaK76uft/ER2zO6yQ41Crn65hgq6Q3nVIUDdUZJXWqUNNs4i/Ub28rFqUUG6ZYGE1Bil7fBPmSGib5xwR5/359/PT64QL87iPCHi2ZcF1eTdzjg3kNnPOrF/qJxSxZPo8ZA4GjiAUSSkR9RUrrve3zqlVXtFHcUUc9lAQiYYSJ8zl8GH/mvMGwpzgqsNWVPnP+fY5tare2qOSoDx0wgT2lM2hCsouq8x2fY2hJLPKaXuvv9vV4XTPTv2GD4wNskIEL7GAE1UOchRXcBAeHg3bZruG39xg2GmzA/zzeNMfbeSRxCo1REZs6rankofY6K6zNZoKKhrNZl2uwXgziVyYgUnktlK/rwuxV3Wk9p+wA+z3qaSbTUDHd41i0op1TlE6r3pHawy7STbJtCEUTHj8e7Q4uch22FtnO4BF/ONAbDMd6Ezz9Eqx4/HlsDyaY760yjxaOwf2xV+QrX5CfC6mRkuVImeSBirstdVXkYjgbqwxX9jUzUUezxYam01W9/SCh33zppp46P6mD6oSmmzuanRupmL+lFBJOdE/USqRVmruouycXdXUzrgzrxWJjIll0/PDefuIRJBg4a0HYQ3J9u+/wPnzuBzpMgJ213fNQ2FLcqpOAME7E2w7NILyl1XSE1BOoUrM60mzqmzqVX9SP6lc0abPhMTBrYeRkoa/J7H3Vd4+1lE/q0vJN9bs5deKrms/c0O7913Xn7g2dXshpYTKncn6gnfqsHh51cUjJMXEw1zr34wckBAGE7xJjCfpnbzQ4EjaH8qASlgOSsUQSbSVxDr0+m7d9jprqJ1CrPmo3cPzEzQdp2nXbrCEXW2z0Gsq0OpqJvqyLEwXtdFY17EPZIKF0oqd0tK9k56rUm9DHLhTUauzp1R+e0r3qPd1+7wN+u6uPPP9pTS8uoKZJJTMp1fdWdbJVgsU2H7w2aj/imoFjkDpW0UcEs/cQB00KO+Q5Vp/wcyDURCOdYVyF6Eip2KGSKZYeDnD/JVU1gwWl+YxELZI4skGa9iHZbEJZVCoaflidyu/ouY1LOqgv6DtbOKMIp4FGTOq+osam2r0BkjzSIJbV3d2Cbl37kZ67tKunn/p5LS5clFJoQ62tfHFCyYlpXbvX1jtHSc3kU4QlewU/vPfxY0yP3z8icGyPYzuCSrgDAohG6vbjEOATc8rHj5TufVNHW/eVzG0ohQRLsQ2M7aK6PfjWh5P9RnAcPiU+KqnXnFezu6lu50O6e+M1fe4zzyibXtPXH0qdbkPx+rc4F2nmOor3j7RzIN2/d0/Ls3mdWvq4ukg6ka7jQYvaOzoSTlSd5mmdDJLKpa11aBNh5ic1NKinQ1AgOyAZDrJ384EIwU6iO4ir2Ywrn2lpIlFRq2/IdATjWbXV52I3AAcLLPGeRvnbypZKKuQKmGJLlaOOOgS/RG9JuWJaJydNlWNT+j9v/j99/EMva3W6qeS9Fa0U93R05881zHxK83M5mNrV/k5Xd27sK3P5Gb32QVory7MapFd03J7Rt67N6fJCT11s+6CbhlE5AFA7kDHWPDZvn2FN5DUQCF1RiG3IKHzPax9JTGTqOjeD+nS/o87xVe0fpzSIn1UKGyiXV9SNVzXsxbnwinoPbqs5OpRWzygd21X9fpW1WL5bJGY9qVQhi/0k9KkzC/raN17R5Ssf6GNTs8pna7o1/LgOGgTyZp3N9tWqpbW0OK/pqQEx7wjVXdOfvzOl7xxESmpOb1fjmkyPlCc2AgtgMoHfGNqSsR36unwKEvV7nlHCwZcD7GQignkNtVxLN3VuCkPfyWpQ+jkV+d4X3+ocqtVOq9nuEsxbKmQWFE2AQhoJHd8/ViLXVg5nMuq0dLLzim7f3dfU4nldeHpWmbNr+i///Xv6D+uR1hbBqXeTMCilwgzoZa6q6zeR3t2GnrlyRuW1j+q4cVbXN4dqY7LrhTixNaY+SKZv55cgBjqe8TdILxBmX2p1NcEmzoRibld+5l9/8dEnfo4phfer9ZK6d7yo6vAJGLOubI6g202q2RupXT1GfXfUiGXA1xF4EWSBY8lmfPF9PGJHlZOBMhMbONcj1ba/q42VJW0Q34pc9fRyjo0tav8kpuNmW+tzQyS8pzfe3tbuTgonhRn0O8S8We32l9TuF/HIgG9YaooSXC/sNyAjdjwWHL89+voRsUGL+I2zOIijDM8sxThZgaFQf4RNOb4NwBpwIp4lK0AV47j5XPFFXH1FjcoNDVpFJUun1B8cKhefU7O1rU4bPJnJa3lmWlPFKTVO7ikzOKvf+MeX1T3p6d13WnqHMLC0gDOZ7+rBrZ7qJ7O69OGnsbk5dQwP+1VNRk3t9zPsJRmAifXP8TggLvb62JUE6hCeJffj97x16ALJQJB/giifDE0YPJ9RAactBrn13qTSBNYcUhnlz/B9SarfUDK/rEESY4eodHeI8EhxCoea7CS0c+3bShAaWs1IndZAazuH2jibI09M8l1PuWighemOTg5jev/dmBZXs5qeW5VK58GhWdU6BR1DnDF1AMyPNv9jWIZQxuQEyh7tn43z0VIND94EJ+MFTJx/TUD1OMijLkYmEJlGr+M8W1pULIV0u3WlSudQw4EGzW1+w2sWlzSoEnhbbxJGRppcu6yt7brmT01qGi8b4RyuXTvRzWs13bwzRkFJMo89YFw/M9BUOaP84E0lmscce0V3iK3DwQRqzm4dx/wwUbwdwXy/+uGw4LcWkInzIwgryHesmZxnNY1A+cZ1GGair2TUQuWt8wMlk3WOwebMmiHvYylsr4jNZTWVaWtmoqHOoEmAT2ly9lkVpmaIoziieFNf+epbWpxvaXXVIWMI0T3CDI6ATR4BphPYsVW1kBuoVMionLuu2djv68XVH+jJ+busg3lgPvaFzrSMncNn9mLAbidpLfR7f58A1Med1ZgeaAlgG8+A2gGEB+RfUJ5N1VXK3tEQL3dy3FWPeJKIZvlsLnFyskY4yWo2V1UxtaPqQQVPugvvDH5PsfctZbId5Up5/ct/cUpr69gvvDkCQ1arLcV6OBq0Zm/vROkUMTSbVKPe0rdff1dPXn5ZE3PntVO9rJPWDBk9YgGtsLCFw2Ps/gNWDh/5zKuF53cO6eF9ECgqmgjY0obcA9Ufs+k7hKXb2rt7pE4PzNmpwj3UUmWkiGQSZRLSPb4nIW1uafdwRyUcyUWC8t4JQJlEtTgxUqcxp7Unu1o6ndZEKa0jUMq715oQn9Lu7hH4Nq/ZqYx6YNldvO7e4brWz3xW79dPq9ddw4NOqoMUclEW2vASEBjKKY9JQZL+85g0S8vvQ7B4zA+kGgX1xvUmhpGK2b6yydtAtK8qCXqp7U+pOZxSPDUkDp2ghpsEYXKy7hGA9y+Q7Bn1anAfJzMYdHVcRZLkCh3b61FDF07P6nC3qcIoh5fsKJECw1aRM2vv8H02fUqnZ0soxY4O9nFGqbOKZTd01J9QBlCRTwAwiAoO6qN+MwR2FlF8SIYT/pgSpyh2k+aBvx2/tzz9FydjffWXfR1j1KPOhEqpp5RezCLJezquHINDF1UojHQqU+AiSeLVLT3Ye1KxdBeJN1VpxbT53h1+A5GwuWxpSotrM8JPED/bunr9QJHdOnH0wV5NuQL2WCHlSSVVbxFXoytaX/+QappSO7akTIHMpdtS6+AhePUhLGuz7QHqXKbeg/PLTimRWcQnOIm2NwWkckSoGKD6gXiIs6oGCdp5OL8bdPvYzSQ2ckEP7j/U5hHeFefi1MfOoDB5lo09YC3UDixZb+VAPqssdKjq8bbOP/Gyjmsn2t5+oFT2gnIZshAS2jJMbjSHOmzU9aGLc4iwpfdv5VUsDjS9+hIbfUl9wsNoiG3W7mq0/YEK7R+puXVDrU5d/fQMqg8AqTxUfuGKsqc/Lc2RMhGbDWhihLJximCP+yg6BgEGLGo6jQ5SwfN0hxd02BqplTnWysbTancPnMMS355QM7us2iEopSjlp57WNrlZN5NTtvd9HWbgYu4JikU39bFL+9qv72pYSevS5dOwcaDDvYomE3jetlBbUqVyS3Pzc0oPesC876rSeU2x9qHS/bexy4b2qlvY+xzgukS6dazcCBXPzlKuONbBW3+kzOyPNL3+rHLz59FSyiMmEi0ZSw/qeDgixP7NH9wbDXA9rnnYCyZR1xgqMQAudVonykc7QDVgG6rX6kTKtr6P676tRicFI86RNTxUOf4dPdheBlNO6vza+9LOTZWnipQcStrfHend66jhcU3nL+Bh8Yjvv3dfcRLY3GRZg8aW3vnBlprsCdCk1ug0XrUIU8kwgYNDiMXHoaCUHvuHmkKCyXQZcPB9bDahMx/+Atj1RUD9GYTkeG2AwgmgHwPxxMd/6d990STZ+zgE9B1gSTz7sTyJ5rRG0RLZw6Sa1DszGWPOAc6FxDODwIobysS2NKL+0kk9q6dWD5WN3VC5kNf5c0+r0SiCJcGwjbjev9HUg82qOp2m2oD1ASi6cYzmpE5rVHwK53Ia55bCzlqsjfcbkWX0AQ5oVzxdVBa7LE2UNOzeVhIGrG6sA//AsH/1f9RvvofdltCsVZwKG8NTx0ke4zhP4iDBEdFCN04BEZN2hEQSqfqPXbXLDHHDuF5ardg5ONig8nyI551UtnxK9cEZzYBUJnM/VLxdVJ6LNZvTMOuEGjCJc32fzOOYhD+ho21KGdD1zVdu6ld/cVmLG+eVbubUa29pb/9I2x80tHm3iZagrgmXPqRivM0rOSN10ny+TLK9Rf31lp7/8LyeePIlPHSVLOfP8ehr0szT7At1RiFH8ezfERhAKDbqkkOMp5Gbg2Y8RrJrGAFCdarShUOtDlyKzePRsLvEFWznWMvZN9WvgnxQj0GvqFYLxIOqbz7c1utXr2rhFPlhFSaRMCcSGX30hQUcTVV7jbdVLPe1shrT1JmzqOmc6v031D5B8vGyJilGTU5NIx0StAbftXfYR5xwg/OL7Wh1YUozJNaj4Z6i5F/qiJTqOLXB3tFKI7EXf+W3vjjGoVbTMdZzGS3ETUuRwuyIk3CzEAPr0WsnmhrVKArdBLnd02jrT/TC6ndRsRzFqWmCc4kYl9J7hI6/eeU1bZw5xYZ6agO8S6mcjg8a2j4CVCxOqnZEyfDdW6ofHGp+Nq3JpbPqR2fRqiOVJ5I4lgmANx4z96QSkyuqNQka7YRmlhYIJQPdu/sa2rcamNbvVyjfnCjewW3jkAw9x3VRS4qnMwkCBvHE6AgigwQtPOIQqhvHcDPEukHvmlLVtxU7+K+A5x09e0kql74AI8o6PjxSa1gD7q3rRzeu67hT0QtkHe1dyiDUXbJTRzo7cVZbV8G7aVBK8hhAjlvGbv/0K9/V2UtdlVY/reSlf6DR8ZvY9/Q4gMPTiPPyQP6UseZ0FueWCbbXqX8dqX6K54T2bx0p0/+Kkiv3NFz5vPNBg1fsD2JMEKLhGcjkHV6ILweoaGyIf+8/VKrziqLt/6leI6O7m2ssuqKnLuXUIJNYmS9hm3fVojP05o/egFFD/cInn9FUuoD9dNR+f0OljV9Wt13BZt9QDQkMKFgtIbnkhIB05zRs3tDJzVua+egX1Z38NY0qB5qZSpIn7hI+CEm5Z9griUCioDr+IDasKjOJZyWEZnMnOqF5U93DOZKepXKoraGN1RGhhQdai82hihipHYvtboTIcxFpUedrGux+VVt3YgDhga7t9fRvv1BAWm3gWRu1PEFNa/rR+5TzANGfeHFFawXKETfaOgRpzSydUQv7OG4TfnpfVlS8oukFNg/C2a90NEVhN146TQh6W5U3/lClT/62YnMX8MYUqlJPUvjtAdpIrgn62TQeNplXs9iBEMr53WPWfaCJ9QP2v6uD5gbhpoRzgrJxCsKrCSUHjNvRQKjTpUyCwm3ye2o+/D1F+99SbRdb6pb11tYJtc6RLp/BoeDqev2y3r23TEXuaUVNVHnyM0hpRicPdnTzbguveonmUE/vv/klIFtPL/3sbyrXukYZJKkjqD8+JMtI5MC0JMJzn8ETv6ro7u+qTP6ZmF5RP4m3RluG9qa5ST7PQEheqfy0eiTgg8yaoskX1ct/SoWVn9bs7HzoYxi4+S9PvzFhUExoGOEwUlTPytHXtXf9y2rc29LW/YG2Dg5Idgn4xJyPPjPS5l5Cb33wkg5PplWLXdGg+Gua/8hvaTo5qXLjBziULE6hoLWz83D5SIcfXIP7VRDIdGiuDClyYY2qtuO6v12B4JwO95ME7n+o1vZXFN35b5qg8JuawF7BwoaOoyiB2RjW2194x/bebhnhwWPT0vRFFVfPY+PEw4DAraPhL+qIhzHEySVvKdf8SyoTX1KG/HCYm9eN+9+U0qcpCBX0Tz//Cc3N/SO9tvlx3R+9pNipz+LKT+taZ526ZUmzla9q+2CkBlnBwnoGyWzreGsP+wEopzKaXLmgZ577BZ1U36GyNoc5kHseVbSzfaL7Ry205ES5mY+pt/97yp+8hleldG+kgmK5JuMULjRF2Wuo0QQ8TeRC44je1FvzirKFIK5ge5agiTU3IiSZ7/0Q0PvvtQjnJqbmdFA5oUD7hLITS7q8vErl+Vk97L+s0amfU37ush52L+t67RRxMq7Uvb9WZfOP9cFJmeygpFiemuZ7dcoTBP4ybW46TdV2VeunCwTxDZwNPQxQUn+QVrtSY8P4szgqB6wbJX5O2v1jpVs7qHAGQo1QMCVrHfscd6HHex9RAhkRwtA/joMZHERvwsLD1RjD2ZNyap9sIRE/p9XL/1EtLn7ztQ+0PL2qo2FZT62d1dnZM7rRfVInHBfPAOs4p0a5cIRBTzZfU37nP6mf+3TI/1KTZ7RLzLuz9zpunYp0YR1LuKk3f/htPUEhq4TaPcRTFmYKanZ6mpqaBEZS/sgs4QLqeFY227iv1M6fqXXmN2iZ5RAB+aA3zm79ePzWaXkcokN2EOiy2nJQaIGZOt7H8KDxWEfViL5C6hPa2ipQ/lvUzIXPqLj288Sxn9JR4jkdjFzxAsaxuus2g4i6aH9HU5u/q3TxJcWLCWo5E7S6TkihyPQKTwcMOUn8SgEeOtRZ3aE6vz6LOxtQBVhSLDdFFaGj9eVlVSuva+uIgnML28sT/1p/pWiX2AtIx4gCISbGIc5PA3Jn9RZQoNG5AyTFXaHyu2Cslin6kYh6AOqsDmvzlAnPKb/4OcVKz2u29JR2qKy9T7srQhXcb08Q64zgI1DObO2vNUk+VI8m1aa+M7V4WsOJF3A8LyqXz1IReEBOeQY8OQ2BD1QBdJ8/s6FTqQJxbl1rp5/Fad2hDpvFRGqA/KGu91Z0og1NFM5pvu6Uao+c287DBI1VNairafATIo2vH79SjDJx/sFP+nxkFH564y1ww7D8oiopWljYQzIFLuCZZLTDgwMJipYRyD3iu1zzHU0evqJ06ayOKjf1sEFtM/O8iotP02Ea0gtEcsCuTGEa+AXjEk+r2koj7QkaMkX1YFa2OKuZ5Y/RZWrwO/F1SAkRzWhjs73YqiYxhyJoCAPj+q6mQaC96E88bb/Wy8dDFWMvSu6V4Dk+0IHfoqbslvKREJJKo4K00siR7LFcKo4bDAQQnqLFfKTcwf/VqN4FIBN4Z35J+Sf+iY6prxySlfcoXs1e+JTa1G9mitdUnjlHEfmKjtrklb2ULj2xwcxPHeallJlawf7yeOQcqdimUu19kuG8bh5ltQtDLLY4BbKxlNgj+xnve+xZTWCQLK8G/rzY8sYALdQ3OAL6fvylbZLIH2wtZMgQN7K0bQkQk6AumqYD1dr9EjEIvIQap0/9PSVKl2iQlvGGkaYmyMRPDlUobZIePc/6yRAG+vEDAndJC7Nn1aAlVp7Bc1JEjkcF8kiSYZLdSUoeSfDWfmOgm3sUwppoUlDFYGDsE/Afqm5jRGZbRFZBXU2bif3xw/lfsEdeQrphYgNHCKQQ5ZPDGSHr9+RDTrnurgZ7f0ySeoFSIt0gcsMRsc84dkAXOD1BWaNCifHBn+nClRc0LH4SMD5DsAe3Ni7pEDt0SeSp2Tk62yXNrz8d1DaRmdDew01GTPC0Jeqq6RiQjToQjBrhH4IahvYsrLbd+cn2gh1y9cfOB1V1/T50QsMBjw9O8F3CqN15lQnmsx2RH37f5/tURCJae1eDzvdJaCeUnr+sYwJ5lXyxDxbFW5FhDXR8fEtnz9X05JVnVRueUidHkptHfU9e1W6lST44q+VMk/rOhArAsna9oYiO1trZl12fAqu2qH4TPpgN2Lv+l4p1aMZ6L94TTxM2/viIMDYcPCyHoMKmnr3w9EnjOIJnNVWoY2iQwoQQRfCWuF20wuEhpVxiU/W7f6Ro+tc1u/CzlB3Oq4oU+kD7HjEpRR9vhDednF2mvz4JvU9S8yypm+qC/oGCYNX9k0rY3WR2l9majHLkcUn20bMPmH6Sytsy6KTAalmtnH6S6twBlfQD9oFzY3QsSAqdhM4f2+JjZBOIHwCoXXMMT1TPfwJhj9SVD8FG/Try73hcJ8iZJIH9+HUcCJhw4hcp+6F+FIZ61C7zRdALpjsgdETleVrhFwjY3wcIED4gIhEvoNLzWpyhZEhqdUw32G6tD4pJRBA5v4wjo2uVnlcX9c3AnBFe2BMDZUBGy1OJMM/uzgJy5duEmkjvNmibpRscUNh+sEpI8oE20vGJPnnsfjjZ8dLqahYwV5brw8Wdryo3+7JaOfroXcrwGQhDen3hbT1jBtKJ4XmTqR52lAG2LaApQGtGtVKFgpZWXmBAIa2dWgz0v6DZzian5DU5s0ppYw8mtZQuLwGayQOp75TTfSYrKPZSD4ox6REqDcF8grYGTcQfBW20RnqvgQZPVViP/aNp8jPERRtr+MzvUB6mL5hwIAwp271FDAQ2lZ8h6yboY68DyhEZcjNzOo19FgAMHghan8loeemfI4U8HpB2NJ417cyAmk4Wu2tFqypMLKpcoX0GmkmnqLAzYDBE2kl6kvEJJIlzmS6THK/ynvkcAiWqS30HyaGg4WmixrZnh8jTv3mYJm4R80UQMZLyHIyfQWpB6GMPGmcOJsamUxZ/bAUb+VUlqKp55kXMkHWAZhGVrywdoQw1ywytZw8QTU8tUSj+CO6fdjRrYMGcj3NLnyOJJVlN5YF/q+rd/R/qVneV4vjS8oc1e+bDKs2vAOFYd2KdtSLNzK0TbsgFB4QobNBe09BtLDEEY6ICLRatK9v846nacKA5gMhCnCOTtzXGsU/HP5bgRMpwEcgfqSQTpwEANGbSeEwuNohN4vmAAC62sponkAZ0TuJIrTYo6Ob+TBgeSpLLGRQnMvybRQNq7scTPwvLWl47p3fvv6npT/yqTj3xHOAJT065w2Ajs0j7u0O/g9BTZNAhAfCw1Vgo/GVvwYLGQgpCGX/HYIUTLKi1h3SE5C2e3Tkvm0Wq/LH6uoiagOtxvKelnshC8oicCzaMGMsaUHmjskfdhF5j+ANrUDFzs5Wc0ge0pUdJez17ZDZOZt5nyikGKhlihzHUePHc53T1nauA9l+kRzIVqu1O3Vx+TFAPbUOsy/MFGClMPOZSOJsbm5NfTSqv3jfvrbo0UC1eizMGGB57yIRBtI/l4gOqaSbMo3jBaGHIyPYGwXHUmBNDvIvQgnqXyjes9JFtHI1DSnroFjUSCsywdFEhLtejOJsh2KfyBaDYUBW6xdMrlzX7t/9ZQ9Q0ObcGfMO3swaNdLwutU+EgH8zBWT0Vk1r26Mt8GLpGGBQKgyM5VTjZGKORxLpvy0U4Sxfnrj5QkpjurOUiN2kNEciJNfnT3eI8VtlucAAZgRlJm9cgLN7tNIGMCBF+7qLKgwoMXhTto1xz4CWONcLw3hLH6WjRS0zE6lGxr42eVorCwk93L2lAgMJ+GViZZYBCNrdHaQC88Ym5cEg1rPvMIa25LiGI4D32aESTyRhYMh2zj/uMp5l4RfOz4MuOvre9V1shBNB8rvHDW3MZnRh2QMB9NdP2rq206RkRyCmj5GFwAFThZ98akIblA3foPR+7e6Bnj8/RYcoptfut7gIak8yy8wdYYMpiz6MBILlaXM3+syAkkrNTMSVY2Rr/cJP08N4Qz/zhc/rbJmiEtrY4DqvvHeomxXm2uyx8QGWVZKJXyMqD+TFEdQAjXOoOzdDlsLr3WOkacwwwcDAhaUZ5WBEm2biZ5lMQnicwK9D0ha8VZISfpVSYY6q2wrGttPxVBQpVb+nNWLc+fkJaqIMJNBGu3wqq0WaJRk+x2fbVMkmSKESjHzRl6ePsLRSQIJZRpbhcADjefK9hG7djeloir7iB68yidjS/CS9SkoUidZQC/kEY1/YK3qzVurphY0Cm490Z7eKNGPUTkvaq9R162Col9YyzA4k9a33abyemU9qdRJQDHHVel1FNuu5Mc+8FLN5tTttHVCt7tDiPmmhMrjqPGzNtdtaQ2JDOrgr8x7E66pCuuS5tPQUTZYa3aSjNsfjWVljJgsxOKEL02UtzhbVqNVJlzzEPmB4Pa4KU09Zspa5WUrux69Ri2XmLbGkVn2gLv2MGbi/URxqu9bSdJ5pjAzXqNIlhrgMxHQbLXqIMUbQ0Cy8epdrXpwHzj3BpF+zWhVdOE1PM5Ta7ujo2N0c/GOjqgobbeMEbH0NhlsjmpnDHj17aqdJqsh5DCxFz33vsMOGaHHlUrrNQN49CkyZbCbUWdpssA3TStkUffs51qyzzjhxvnH3kN5DHDvrE0rTevbZZ3R0+6NMQ72lMxt0lBnQ7tHjyVMfXSwTY2kLJJlmvLdDGw+nZvx8UKmoQu/DIyQTlDR3KXUUyGiy2G9URTqVJpAIONRhUyawgaTanS45m/2Xmy/8izH3WbjVJUzAqT4GtUPMc5J/QL8de4cg1AAjf7DT0BE9siHqPMDaO3jDBEF/cZJEdpO6Kv3EDLZ4ctLQIUXfFHZVpO/41u2KLi8NdfHZT+t//cnXdP7SxyE8oUqjTR7YZV+sRXw+ogEzUScMgGRq7LXC5FTfCQCz3ZX6SOViBrABmkqSlZzwY4fRyEaryWZsorheu1nGPFJMVwwIBX4OCRUpqLEaubxfZeO8xd+PCOBIj7fV9gCJUZUEaBPP4e6IMoUDFuuytl3bQ+qefRgzhEnu+w+41r1dZuAA/Yf1pLb2R3pmYU2l6Gt6/Z37KlEzrcJ0z7C20ZoUnMxjBi2E4h5gHeaRUvJgP2gF2RWm9qjqRpoVtdhgCGeI15scIiXfVhMCP6DbheDIlWQ2YELTVNIcBzNw3NNF9kbOuBMcE0qPHligWm0Uk0J9kxSI+oQL388Uh6Be2CRVNeZS+yH+omZWV1RtAXTT4DhnDqeX8rr+8JYuLa5BCN6aC+U4jiuGjMb+0pqUARZGOc5h9w4ZriVBa9gjuzSBlplFwUFsFscWYgn/hg0PUIm+Uyo2RiBSFb0fDmhhpSOkhMtv0Y7mz4hYaYQCqU5HIDiFf6a7y4ZdIHIcdM2ZXXAtfnfhyBzFBPzoYuNpusQtmNOh57CwsKy//d4NXXr+5aDqPpVDwppeIcleuuav8Ro/DgkdRDEOoYZk9SFk9KjzRNTFoJYz2Vr4y1W9UWsUdOE4rJLsGS76d7ubuHEcx/SQtiFPjI5r2ABEDBjS6TCOUq1UUQLHKzOOvNDxEmIduAOjqiec3yLQm1EM3vruF47ugW5O4UiWVzY0+vo3tH94GJJln2uGGD56aMIVwHE918E/cCrQMKLLVT3c1P72OzjDfUVb3LMwRK+dHHJGWCBIEg5Z7CYp3HJHkPZnE8uboLL+PEYXRhG01I73KBQzMYG3tac0gZkMBWJUO2yGU8MAHQ6m22Ek2Zsk/PSsRTgTjFPfwDvO/tSKFi8yPs3U1YPbd7V+rshMTiv4AV/fLHemwyXZm7c93qlNoFvbVuXuN/ArlPpxXtGX/vpVbAXs6XjFRgacYfz36BRIGL+zWhn99c0E1NEPXyAFqs9RbU6BiOyB68SzMRFFeoZsh/mQkCt6ExzvcyIcRioqh41FOIwEMdLp2ZBgfG6O5imDCp//yLwunn9O//t732bwIaXtw2Nu7UE77B4gymmY60kBnwVB8D0a1GP8JT08R555mVoRhY8oaxUJQmHjqB0Oxk3D4DnhlPXZKhAcDwt27YSQTBhhtHNhUpCEMAzuDaijpinOeure9wIOgWTBdFEpOxc7HhSVjfE51g7OCw8VmNaFQNvu1HSkd5FWk7tfNlaWlf3ma9RkUd8iqTIOzMOH1qMcEjdaCSYTnIuJQLKYUj/UazgO04uWl6c0AecSOAzHvS5t5ThdGud1rBVUL4X38qCQYZlzQzMhyeJpVCKF08ggBadFXb63XcbxyD2O9y0ARvaYKxJjBsaaAoH2xLbjUDNhDQ8fMZ2GBnh+LY36MkODq5+bm2Jii7nufEcfeWKF8w2xfT1aaTDQErR37nvMBc/eQXoevzSvRqi7QXj0Gy9fCW/4B2nBTTsOuB1BgL+zPhieOY9rYzdjhzJ27X1W6gIzklwQ7Q3ERRzruZqgDbx2uwQpOJUmHvqCva7REJ4SiOdu7oDrdbDBNhXuNoxNUt2uAxAqlRbz3iUtFcDAe7e1cmqaGXHGO8lkjsMteXhvHJPTPTN/fJcoRLHnLHWdTIohhQJQjdYksuS2DN/8gbNO4VxSXKRH8G7Wm3AVCBTiHhOCYFV71yROwtJlbQgZx0OXIOyk+3zumkAoroFAOjAlAwRLYqNWezsEx6sw7YTKOga6Buvc0ddp4l3r3EdRo/9+cMI8G9NNVx9s6sIFM83qiYYwuukMKE+OGFnbMHVL0XpAiIepaGLnxLdjKHpvcwuOY+DmAod4iTSVMHPX6vbYxYSNIUVzKIgedbH02oDujDcJfQPUOk33NoYU7daTxDrf/WKNsHp2Oo/yStZIY79uRbs84nNdiDJTkjiUNOPSTTKX/OlFPf3cR3T1D/+GG01aVNWKSBYQjjo7Do7AyN04kmSvtvUgPUhMkv1EnjVg99ESA3EOzyYweDtuPLT7bnnjlAjM3Rou37bh+U6rVA+1i5E+UU2heVJDHcD0SMA9ByI+txo4c2fX2KfjpyFgs1UJ0oM9wLNHjgs76cEIx12DeHvADu23GLWfXgs1bqW0fvqcNhZf1d17t3T54lOM03ADJugoCQFJRrwyMDFFrE4Rjx1pkoxmR/RTPHeeiAHVetzokYCbwfYsP3MGQY6wFRNjGeJC4S7Tuo2a6qip1dPI3yX/aSYeYjio0Nu3TaIeofTBGkOgxYD5Gg5jYa5uonEonk2NHpU8skjQKCeU+ah7RlkmOwDKMcaiU2zSt7HOUAi+fudtnXm2TOGXda1lLBejUWtE5Hgb5A/jXEDrkYeiT6wJzGzW9oOXs5i5UnA0lig8ZYOeT7OPSKCKEOtqlPEd3PJUuz+RCcEAqsxWM6sOEkyCQX3RhDeMuiAz1N7JLVsL3MWrQhQainqSdnGunYU9sVte7JIvugwHAuBiyzq9znDDjW9rm1bcmefX8LAM3bjmw876YGmHMXA+Wkhxiuv37CisQy5RJukFwGaq1WME7hBv6ocMoHa5+yTJxZKI1EWoyJW0vO/4ckcXlSAFclWMoBDMu49qu+JWcPC2C4c5IV4GAyUztwDNCda0w+ET61BRY4NDQowFPa6E5fCq2ChYMk5+uUo8vHRxXa+8sUVHeAnJkp1y3RRMNgb2iQMDUTMJBxhBmNM5Q7qoHN9CDRjC4QQDVAdSz1dHJKCYHZv0ppEoRDonHHKMRW8Jup/unCViUQdx/gkxcshteNAGEWOmhao452ByEOy8EhsHztkpGCz3OTfFTEsK5+Z47Pvx7dRGhIFRVIcxSWxxTq9dvadXvn1NP/tTT5CxdJl6NGriQhwb4jYctYNNs1YHF9pl39Fs8iabMkEWKZuCgDi6E9STmxe7eC9QEVwjZwT69Ek3MkYfeNB6tcamyJyzdIC9OFzM5ynm4ii4ZrDliGOdgvnciGP94LpoRxPGO6swFnV4QYtIlxJ4RfvzEQDedaBklomLZInKQV6feOGs/vSvfkBNZ1IXVsohkzF9ZryrbQYaQ7jYxG7sMLMUsyLb1sOdIwo+B5qamwvudbqQJFgCu0iJnCp1yO79iOMlO4g+BSTrQWCeFlgD/DnEYaSo07hcF5FJ2Dn5N9dULak05QOjo4jQYifmOAptTAJzHwXrOp2yFvRYu0bcjaFi5pB7HPkMHSf6GEnmVJfnp+hxTOnLf3FV/+pXPhI0Lp1JameH0cxZBnDZk++UyeS4FtVyg4X4PnOaI4qz+YLtwHe0oBbEJBu7/3MAhwZLyBxKA+mcYKZ5JuGah4bSrusZi4EuMhR4DQy65IyNpksfBBK8quNimhK/h227SLJK9SsczyRSMok3Bm44EXVoOjqqwxS6gazVsWbB1BT3SqQI6k2EMUX17UtfvqG3rt+mvW11b9JMJZNnVjSWbLEM04Z1vD13wCWZjcN5UZMsZ1mQeRTY2cdzWlXNUZcVbPRGNt0Arcb3Clo6CbyhbSCBCzTA3Ts4hglUtwkjp5hDS1PMtZez5AZI9oRGZxpGGcEkkaRTyC7SbrscAQBwvpiCgWVu0nJIClUADPnhw7vUYeqEiiwtuIJOzc7o13/hvL7z3qaunKPThNE5izDMaWMijVqPO2vAtSCo1RVs+lc+d/GLdS6yvcMwONJw3Bqgy0WmHKx+XeIhlCIBJ6U4fIi2ZBpk8rYp3xJ7xNRumryvCiCYnqENXWRkhLVOkJTVrkn9pEEaZaRjxOEc0qjGWXiCAJ+BGVlULUNmk3Xn19MdkJmlFbe1u6NvvfoDypD7FJO44eTUIhLu6Xd+/1XNcNdMuYRDweZ9rQ6a0+zWNOmxFC5Ur+MQf/3nP/TFjmug1BoTxK8SFSkP2ty+v0vFmTIihOztV3A8qCmccr2xQcXMyL3BXHac8SwPxtXoq68tzXI+ZUgYYPBbraI+IeHF2WIbWdTdmYAbOe5rJAHdJsalvwz2TlRjmJZxrjKNVMykzy1BIDNt7+/qxuY17Wzug1kH+gB4mS00OPaQOVPusTggvSLFsnm1O1T0Kvv4kIwOubst9o0/+Gejes0xCjsiEOepZW7jdNy2chI8GjZDVl6tMjc2QXwiyPaom0xzT0SG8n6HPsaAom+fNKtIzBq3zFIq0sH1Re1FHA7cNhs4TmAHQ+CgR6RToCHXW933M5NaOIkOzwFt8T43R968ua+HAO0ETMgtIBGkOKxSbsTOi4DwMwzz3bi7o52H3AQ2O0EuCbAnPx3yHxp4j/kcuW4FqOYcMI2xT0wWGW+ssSMmlyi0VrkVp95iDoY65KQHc8jpWrjxPmo8ZCPDZDY4kxjfFZD2Ccc6N8whrS5qw75RbdsvUM+EwcO0cSvr90iuC/QeGq0q6wHpID6BbXaAg1UK0TubcW7YqmhuAQfFlGE2P2LAYUp3uY09SUK7AIH142PuPh3qmY9O6nCbuMr+7IGdgzZok2MBVNwKTD9Qcj9kVvOQ6nQqV2ZDLYZzuPGDW8QbHaYJQRU57uocgf06qND8/CyOpQ8z4CiB2YXcSvsgcI0gEtIkQXQbj1mmz2dCR+R8SY61dzMeTSbL6pxwRxtgYWDUxLr1Om1vPKIdk+c+19doeafxDcTDIbWbPcr4KRo2E/N59uP6J2X/Oc+RcsNz/VBtBvcmcGSlMoVlitAnDTTzlz/7oS/mgWAu+jjyOKsvTRMCSFveeZ95FIy/iQQj+hQdDBf/FLJ1Y7cki7g84fzPac/mzj6OiKGCXbto1iQWPdiiuoYiZriRqgPSOSY2+dacAWraY6Dczsq9wkOaMvuHdXBpnvgFBo5x32KqgaSparuEwTFotabp7maZhOq1CW2Yk4Fs5yTOiFiZcMH+OeaEKrhh0wweGUq4PRUOHTVZkE3l6RGmyYab7ZFOb0zjTRkwJ+j6/kCjk3ymTPpko+YDPb1Ws8ErxBIHbXJ11HqOHkcO+zqmNH/MaIjbAHHa0PZ+7le4jDhAYseHOAoc1uZD5tFwFq6Et5j0nQy2BCMpK1ZpsFQq7KFHGKMCn0AFu/yHBBGD8AAVLRHipmjMlNm3NYz/kAGzwKmxtz57/P87Su0ZFCF3bwAAAABJRU5ErkJggg=="
PALM_TREE_BASE_64 = PALM_TREE_BASE_64.encode("ascii")


class TestApp(App):
    def __init__(self, client: Client = None, config: Dict[str, Any] = None):
        super().__init__(client, config)
        self.index = None

    @get("resp_string")
    def resp_string(self) -> Response:
        return Response(string="A String")

    @get("resp_dict")
    def resp_dict(self) -> Response:
        return Response(json=dict(string="A String", int=10))

    @get("resp_obj")
    def resp_obj(self) -> Response:
        return Response(json=TestObj(name="Foo"))

    @get("resp_binary")
    def resp_binary(self) -> Response:
        _bytes = base64.b64decode(PALM_TREE_BASE_64)
        return Response(_bytes=_bytes)

    @get("resp_bytes_io")
    def resp_bytes_io(self) -> Response:
        _bytes = base64.b64decode(PALM_TREE_BASE_64)
        return Response(_bytes=io.BytesIO(_bytes))

    @get("resp_image")
    def resp_image(self) -> Response:
        _bytes = base64.b64decode(PALM_TREE_BASE_64)
        return Response(_bytes=_bytes, mime_type=MimeTypes.PNG)

    @get("greet")
    def greet1(self, name: str = "Person") -> Response:
        return Response(string=f"Hello, {name}!")

    @post("greet")
    def greet2(self, name: str = "Person") -> Response:
        return Response(string=f"Hello, {name}!")

    @get("space")
    def space(self) -> Response:
        return Response(string=self.client.config.space_id)

    @get("config")
    def config(self) -> Response:
        return Response(
            json=dict(
                spaceId=self.client.config.space_id,
                appBase=self.client.config.app_base,
                Client=self.client.config.api_base,
                apiKey=self.client.config.api_key,
            )
        )

    @post("learn")
    def learn(self, fact: str = None) -> Response:
        """Learns a new fact."""
        if fact is None:
            return Response.error(500, "Empty fact provided to learn.")

        if self.index is None:
            return Response.error(500, "Unable to initialize QA index.")

        res = self.index.embed(fact)

        if res.error:
            # Steamship error messages can be passed straight
            # back to the user
            return Response(error=res.error)
        return Response(json=res.data)

    @post("query")
    def query(self, query: str = None, k: int = 1) -> Response:
        """Learns a new fact."""
        if query is None:
            return Response.error(500, "Empty query provided.")

        if self.index is None:
            return Response.error(500, "Unable to initialize QA index.")

        res = self.index.query(query=query, k=k)

        if res.error:
            # Steamship error messages can be passed straight
            # back to the user
            return Response(error=res.error)

        return Response(json=res.data)


handler = create_handler(TestApp)