## GH-TL
Github Timeline Embedder

<br/>

## How to use?

Just use it as an image tag

<img src="images/image_snippet.svg" width="60%"/> 


Result

![](https://gh-tl.now.sh/svg?user=joelibaceta)

## Options


### Zoom ###

#### 0.5x ####

```html
<img src="https://ghtl.vercel.app/svg?user=joelibaceta&zoom=0.5"/>
```

![](https://ghtl.vercel.app/svg?user=joelibaceta&zoom=0.5)

#### 0.25x ####

```html
<img src="https://ghtl.vercel.app/svg?user=joelibaceta&zoom=0.25"/>
```

![](https://ghtl.vercel.app/svg?user=joelibaceta&zoom=0.25)

### Shape ###

#### Circle ####

```html
<img src="https://ghtl.vercel.app/svg?user=joelibaceta&shape=circle"/>
```

![](https://ghtl.vercel.app/svg?user=joelibaceta&shape=circle)

### Dark ###

#### true ####

```html
<img src="https://ghtl.vercel.app/svg?user=joelibaceta&dark=true"/>
```

![](https://ghtl.vercel.app/svg?user=joelibaceta&dark=true)

### Color ###

#### Blue (#38507a) ####

```html
<img src="https://ghtl.vercel.app/svg?user=joelibaceta&color=38507a"/>
```

![](https://ghtl.vercel.app/svg?user=joelibaceta&color=38507a)


#### Red (#dd4b3c) ####

```html
<img src="https://ghtl.vercel.app/svg?user=joelibaceta&color=dd4b3c"/>
```

![](https://ghtl.vercel.app/svg?user=joelibaceta&color=dd4b3c)

#### Pink (#ff4081)

```html
<img src="https://ghtl.vercel.app/svg?user=joelibaceta&color=FF4081"/>
```

![](https://ghtl.vercel.app/svg?user=joelibaceta&color=FF4081)

#### Purple (#8e44ad)

```html
<img src="https://ghtl.vercel.app/svg?user=joelibaceta&color=8e44ad"/>
```

![](https://ghtl.vercel.app/svg?user=joelibaceta&color=8e44ad)

<br/>

### How it works?

1. Receive a http request with the github username whose timeline want to embed
2. Make a GET request to github.com to get the profile page source code.
3. Scrap the html code to extract the timeline svg tag.
4. Prepare the final svg to return.
