// var getTextButton = document.getElementById('testText');
// var getSuggestionsButton = document.getElementById('generateIdeas');
var textArea = document.getElementById('story');
var graphButton = document.getElementById('visualisationButton');
var mydiv = document.getElementById('tabletop1');
var svTable = document.getElementById('sv-table');
var ideasTable = document.getElementById('ideas-table');
// getTextButton.addEventListener('click', async function() {
//     console.log('button clicked');
//     console.log('story', textArea.value);



// });



// getSuggestionsButton.addEventListener('click', async function() {
//     console.log('button clicked - get suggestions');
//     console.log('story', textArea.value);


// });



graphButton.addEventListener('click', async function() {

    await fetch("http://localhost:8080/getGraphs", {
            method: "post",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({ keyword: textArea.value })
        })
        .then(response => response.json())
        .then(async text => {
            let t = text;
            console.log('this is what we got back', t)
            var ifrm = document.createElement("iframe");
            ifrm.setAttribute("srcdoc", t[0]);
            ifrm.setAttribute("frameBorder", "0");
            ifrm.style.width = "550px";
            ifrm.style.height = "500px";
            ifrm.style.frameborder = "0";
            document.getElementById("plot-bar").appendChild(ifrm);
            var ifrm1 = document.createElement("iframe");
            ifrm1.setAttribute("srcdoc", t[1]);
            ifrm1.setAttribute("frameBorder", "0");
            ifrm1.style.width = "550px";
            ifrm1.style.height = "500px";
            ifrm1.style.frameborder = "0";
            document.getElementById("plot-bar").appendChild(ifrm1);
            console.log('graph should be there')

            // third graph
            var ifrm2 = document.createElement("iframe");
            ifrm2.setAttribute("srcdoc", t[2]);
            ifrm2.setAttribute("frameBorder", "0");
            ifrm2.style.width = "550px";
            ifrm2.style.height = "500px";
            ifrm2.style.frameborder = "0";
            document.getElementById("plot-bar").appendChild(ifrm2);
            console.log('graph should be there')



            // 
            fetch("http://localhost:8080/parseKeywords", {
                    method: "post",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },

                    body: JSON.stringify({ keyword: textArea.value })
                })
                .then(response => response.json())
                .then(async text => {
                    let t = text;
                    console.log('this is what we got back', t)
                        // console.log(Object.values(t));
                        //Send english settings first
                    data = {
                        'language': 1000,
                        'location': 2840
                    }
                    await fetch("https://keyword-research-api.herokuapp.com/settings", {
                        method: "POST",
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    // send keywords
                    keywords = {
                        'keywords': Object.values(t),
                    };
                    await fetch("https://keyword-research-api.herokuapp.com/keywords", {
                        method: "POST",
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(keywords)
                    });

                    await fetch('https://keyword-research-api.herokuapp.com/search_volume')
                        .then((response) => {
                            return response.text();

                        })
                        .then((data) => {
                            data = JSON.parse(data);


                            // console.log('data', JSON.stringify(data))
                            // console.log(typeof JSON.stringify(data))

                            fetch("http://localhost:8080/max5", {
                                    method: "post",
                                    headers: {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json'
                                    },

                                    body: JSON.stringify({ listLists: data })
                                })
                                .then(response => response.json())
                                .then(async text => {
                                    let t = text;
                                    console.log('this is what we got back from the max 5', t)
                                    document.getElementById('top1kwr').innerHTML = t[0][0]
                                    document.getElementById('top1vol').innerHTML = t[0][1]

                                    document.getElementById('top2kwr').innerHTML = t[1][0]
                                    document.getElementById('top2vol').innerHTML = t[1][1]


                                    document.getElementById('top3kwr').innerHTML = t[2][0]
                                    document.getElementById('top3vol').innerHTML = t[2][1]


                                    document.getElementById('top4kwr').innerHTML = t[3][0]
                                    document.getElementById('top4vol').innerHTML = t[3][1]


                                    document.getElementById('top5kwr').innerHTML = t[4][0]
                                    document.getElementById('top5vol').innerHTML = t[4][1]
                                    svTable.removeAttribute("hidden")

                                });








                        })

                    fetch("http://localhost:8080/parseKeywords", {
                            method: "post",
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                            },

                            body: JSON.stringify({ keyword: textArea.value })
                        })
                        .then(response => response.json())
                        .then(async text => {
                            let t = text;
                            console.log('this is what we got back', t)
                                // console.log(Object.values(t));
                                //Send english settings first
                            data = {
                                'language': 1000,
                                'location': 2840
                            }
                            await fetch("https://keyword-research-api.herokuapp.com/settings", {
                                method: "POST",
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify(data)
                            });
                            // send keywords
                            keywords = {
                                'keywords': t.slice(0, 20),
                            };
                            await fetch("https://keyword-research-api.herokuapp.com/selected", {
                                method: "POST",
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify(keywords)
                            });

                            await fetch('https://keyword-research-api.herokuapp.com/keyword_ideas')
                                .then((response) => {
                                    return response.text();

                                })
                                .then((data) => {
                                    data = JSON.parse(data);

                                    // console.log('suggestions', data[0])
                                    var keywordsList = Object.keys(data);
                                    var volumeList = Object.values(data);
                                    var results = [];
                                    for (var k in keywordsList) {
                                        var keyword = new Object();
                                        keyword['Keyword'] = keywordsList[k];
                                        keyword['Volume'] = volumeList[k];
                                        //keyword['Competition'] = '';
                                        results.push(keyword);
                                    }


                                    // var final = Object.entries(results);
                                    // console.log('ideas', results)
                                    var final = []
                                    for (i = 0; i < results.length; i++) {
                                        final.push([results[i].Keyword, results[i].Volume])
                                    }
                                    // console.log('final', final)
                                    fetch("http://localhost:8080/max5", {
                                            method: "post",
                                            headers: {
                                                'Accept': 'application/json',
                                                'Content-Type': 'application/json'
                                            },

                                            body: JSON.stringify({ listLists: final })
                                        })
                                        .then(response => response.json())
                                        .then(async text => {
                                            let t = text;
                                            console.log('this is what we got back from the max 5', t)
                                            document.getElementById('top11kwr').innerHTML = t[0][0]
                                            document.getElementById('top11vol').innerHTML = t[0][1]

                                            document.getElementById('top22kwr').innerHTML = t[1][0]
                                            document.getElementById('top22vol').innerHTML = t[1][1]


                                            document.getElementById('top33kwr').innerHTML = t[2][0]
                                            document.getElementById('top33vol').innerHTML = t[2][1]


                                            document.getElementById('top44kwr').innerHTML = t[3][0]
                                            document.getElementById('top44vol').innerHTML = t[3][1]


                                            document.getElementById('top55kwr').innerHTML = t[4][0]
                                            document.getElementById('top55vol').innerHTML = t[4][1]
                                            ideasTable.removeAttribute("hidden");

                                        })
                                        .catch(err => {
                                            console.log(err);
                                        });




                                })

                        });

                });
            // 



        });
});