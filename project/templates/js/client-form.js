/*
    3.this the container under which the whole form will be append
 */

let container = document.getElementById("container")
let dict;

function func(params) {
    /**
     * In FormCondition function it takes index (index value from for loop) and checks condition for each input type to validate it and append it inside its parent tag.
     */
    FormCondition = (index) => {
        /**
         * 
         */
        questionTag = (index) => {
            const question = document.createElement('h4');
            question.className = 'question';
            question.textContent = params['data'][index]['question']
            container.appendChild(question)
        }
        if (params['data'][index]['type'] == 'text') {
            questionTag(index);
            // answer field
            const textTag = document.createElement('input');
            textTag.type = 'text';
            textTag.className = 'text-input';
            container.appendChild(textTag)

        }
        else if (params['data'][index]['type'] == 'textarea') {
            questionTag(index);
            // answer field
            const textareaTag = document.createElement('textarea');
            textareaTag.className = 'textaera-input';
            container.appendChild(textareaTag)
        }
        else if (params['data'][index]['type'] == 'dropdownWidget') {
            // 
            questionTag(index);
            const selectTag = document.createElement('select');
            selectTag.className = 'select-input';
            container.appendChild(selectTag)

            params['data'][1]['options'].forEach(element => {
                const optionTag = document.createElement('option');
                optionTag.className = 'option-tag';
                optionTag.textContent = element;
                selectTag.append(optionTag)
            });
        }
        else if (params['data'][index]['type'] == 'checkbox') {
            questionTag(index)
            const checkTag = document.createElement('checkbox');
            checkTag.id = 'check-btn';
            params['data'][index]['options'].forEach(element => {
                const optionTag = document.createElement('label');
                optionTag.textContent(element);
            })
        }
        else if (params['data'][index]['type'] == 'radio') {
            questionTag(index)
            const radioTag = document.createElement('radio');
            radioTag.id = 'radio-btn';
            params['data'][index]['options'].forEach(element => {
                const optionTag = document.createElement('label');
                optionTag.textContent(element);
            })
        }
    }
    for (let index = 0; index < params['data'].length; index++) {
        FormCondition(index);
    }
}


/* Initially the code starts from here
    1.Here the api attr calls the api provided in fetch api
    2.the valid json is sent to func() function
*/

let api = fetch("/api/form/{{id}}")
    .then(response => {
        return response.json()
    })
    .then(data => {
        func(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });