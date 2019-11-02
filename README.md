## GH-TL
Github Timeline Embedder

<br/>

## How to use?

Just use it as an image tag

```html
<img src="https://gh-tl.now.sh/svg?user=joelibaceta"/>
```

Result

![](https://gh-tl.now.sh/svg?user=joelibaceta)

## Options

### Zoom ###

#### 0.5x ###

```html
<img src="https://gh-tl.now.sh/svg?user=joelibaceta&zoom=0.5"/>
```

![](https://gh-tl.now.sh/svg?user=joelibaceta&zoom=0.5)

#### 0.25x ###

```html
<img src="https://gh-tl.now.sh/svg?user=joelibaceta&zoom=0.25"/>
```

![](https://gh-tl.now.sh/svg?user=joelibaceta&zoom=0.25)


### How it works?

1. Receive a http request with the github username whose timeline want to embed
2. Make a GET request to github.com to get the profile page source code.
3. Scrap the html code to extract the timeline svg tag.
4. Prepare the final svg to return.