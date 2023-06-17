from langchain.document_loaders import PlaywrightURLLoader

# TODO: add more loaders
class DataLoader:
    def load_urls(self, urls):
        playwright_loader = PlaywrightURLLoader(urls=urls, remove_selectors=["header", "footer"])

        return playwright_loader.load()
