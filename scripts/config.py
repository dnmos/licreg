import os
from dotenv import load_dotenv


load_dotenv()

# DB
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Filters (file names .json)
# FILTERS = ["federal-area", 
#             "license-status", 
#             "plot-status", 
#             "russian-regions", 
#             "type-of-minerals", 
#             "type-of-work"]
FILTERS = ["plot-status", 
           "russian-regions", 
           "type-of-minerals"]

# Paths
PROJECT_PATH = "/home/www/licreg/"
#PROJECT_PATH = "/home/dm/app/python/licreg/"
FILTERS_PATH = PROJECT_PATH + "data/licenses-registry/filters/"
STATUS_PATH = PROJECT_PATH + "data/licenses-registry/status/"
JSON_RESULT_PATH = PROJECT_PATH + "data/licenses-registry/json/"

SQL_QUERIES_PATH = "scripts/sql/"
CREATE_TABLES_QUERY_PATH = PROJECT_PATH + SQL_QUERIES_PATH + "db_create_tables.sql"
DROP_TABLES_QUERY_PATH = PROJECT_PATH + SQL_QUERIES_PATH + "db_drop_tables.sql"

# CSS selectors
LICENSES_SELECTED = "#cd42f192ca53498dae511d0638a81829 > div"

REGIONS_WIDGET = "#bf074f6f6c994c49b33efd267915a9b3"
REGIONS_WIDGET_ROW = "#bf074f6f6c994c49b33efd267915a9b3 .rb-filter-body-container.opened .rb-filter-list li:nth-child"
REGIONS_WIDGET_BUTTON = "#bf074f6f6c994c49b33efd267915a9b3 .rb-filter-body-container .rb-filter-apply-button"
REGIONS_WIDGET_HEADER = "#bf074f6f6c994c49b33efd267915a9b3 .rb-filter-header-container"
REGIONS_WIDGET_UNSELECT = "#bf074f6f6c994c49b33efd267915a9b3 .rb-filter-body-container .rb-filter-unselect-all-button"

NEXT_PAGE = "div.dx-page.dx-selection + .dx-page"
LAST_PAGE = ".dx-pages .dx-page-indexes .dx-page:last-child"

TYPE_OF_MINERALS_WIDGET = "#fe41d295d6db47b8948a12c3504ddaec"
TYPE_OF_MINERALS_WIDGET_ROW = "#fe41d295d6db47b8948a12c3504ddaec .rb-filter-body-container.opened .rb-filter-list li:nth-child"
TYPE_OF_MINERALS_WIDGET_BUTTON = "#fe41d295d6db47b8948a12c3504ddaec .rb-filter-body-container .rb-filter-apply-button"
