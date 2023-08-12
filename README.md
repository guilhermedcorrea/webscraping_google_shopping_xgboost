#Aplicado Modelo Flyweight


```Python
def calculate_probability_of_sale(row):
    price_difference = row['sugestao_preco'] - row['precoconcorrente']
    std_deviation = row['preco_real'] - row['sugestao_preco']
    if std_deviation == 0:
        return 'N/A'
    z_score = price_difference / std_deviation
    probability = 1 - norm.cdf(z_score)  
    return '{:.2%}'.format(probability)

def train_and_predict(csv_file_path):
    dados = pd.read_csv(csv_file_path, sep=";", encoding="latin-1")
    dados.fillna(0, inplace=True)
    dados[['preco', 'margem', 'precoconcorrente']] = dados[['preco', 'margem', 'precoconcorrente']].applymap(
        lambda k: float(str(k).replace(",", "").replace(".", "")))

    object_columns = dados.select_dtypes(include=['object']).columns
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    encoded_data = encoder.fit_transform(dados[object_columns])
    encoded_columns = encoder.get_feature_names_out(object_columns)
    encoded_df = pd.DataFrame(encoded_data, columns=encoded_columns)

    dados_encoded = pd.concat([dados.drop(object_columns, axis=1), encoded_df], axis=1)

    X = dados_encoded.drop("preco", axis=1)
    y = dados["preco"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_grid = {
        'n_estimators': [100, 500, 1000],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7]
    }

    regressor = XGBRegressor(random_state=42)
    grid_search = GridSearchCV(regressor, param_grid, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_regressor = grid_search.best_estimator_

    results_df = pd.DataFrame({
        'nomeproduto': dados.loc[X_test.index, 'nomeproduto'], 
        'precoconcorrente': X_test['precoconcorrente'],
        'preco_real': y_test,
        'sugestao_preco': best_regressor.predict(X_test)
    })

    results_df['diferenca_preco'] = results_df['sugestao_preco'] - results_df['precoconcorrente']

    results_df['probabilidade_venda'] = results_df.apply(calculate_probability_of_sale, axis=1)

    pd.set_option('display.float_format', '{:.2f}'.format)

    return results_df

```


<b> Faz previsa de Preço para venda com base nos valores recebidos pelo Decorator e uma checada na base de dados no SqlServer. Tambem faz um calculo de probabilidade  e retorna o resultado junto </b>







```Python
 
def price_analysis_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        url_produto = kwargs.get('url_produto')
        ean = kwargs.get('ean')
        
        product_info = func(*args, **kwargs)  
        results_dataframe = analyze_price(product_info)  
        
        return results_dataframe
    
    return wrapper


@price_analysis_decorator
def analyze_price(url_produto, ean):
    return url_produto, ean



class FlyweightProxy:
    def __init__(self, proxy_options: dict):
        self.proxy_options = proxy_options

    def create_driver(self, options) -> Chrome:
        return Chrome(
            executable_path=ChromeDriverManager().install(),
            options=options,
            seleniumwire_options=self.proxy_options
        )


    def get_driver(self, options) -> Chrome:
        if not hasattr(self, '_driver'):
            self._driver = self.create_driver(options)
        return self._driver
```



<b> Padrão de Projeto Flyweight | Decorador price_analysis_decorator recebe </b>






```Python
 def make_request(driver: Any, url: Any) -> None:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    ]
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": random.choice(user_agents)})
    time.sleep(random_delay())
    driver.get(url)
    time.sleep(random_delay())
    scroll(driver)




def extract_and_analyze_price(url_produto, ean):
    proxy_options = {
        'proxy': {
            'http': 'http://your_proxy_ip:your_proxy_port',
            'https': 'https://your_proxy_ip:your_proxy_port',
            'no_proxy': 'localhost,127.0.0.1',
        }
    }

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en-US")
    options.add_argument("accept-encoding=gzip, deflate, br")
    options.add_argument("referer=https://www.google.com/")

    proxy = FlyweightProxy(proxy_options)
    driver = proxy.get_driver(options)
    driver.implicitly_wait(10)

    time.sleep(1)

```


<b> Implementado Proxy e Headers </b>