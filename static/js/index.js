//Fetch List of Distinct Genre
const fetchGenreList = async () => {
    const options = {
        method: 'GET',
        mode: 'no-cors',
    }
    const response = await fetch('/genre', options)
    const data = await response.json()
    genreList = data.map(genre => {
        let option = document.createElement('option')
        option.textContent = genre
        option.setAttribute('value', genre)
        return option
    })
    $('.advanced-search select').append(...genreList)

    // document.querySelector('.advanced-search select')

    // $('.dropdown-mul-1').dropdown({
    //     data: data,
    //     limitCount: 40,
    //     input: '<input type="text" maxLength="20" placeholder="Search">',
    //     choice: function () {
    //         console.log(arguments[1].id, this,);
    //         console.log($(`.dropdown - mul - 1 select option[value = ${ arguments[1].id }]`).attr('selected', 'selected'))
    //     }
    // });
}

// Fucntion to Delete Selected Record
const deleteRecord = async (id) => {
    let formData = new FormData()
    formData.append('id', id)

    const options = {
        method: 'POST',
        mode: 'no-cors',
        body: new URLSearchParams(formData)
    }
    const response = await fetch('/delete', options);
    const deletedMovie = await response.json()

    console.log(deletedMovie)
    submitSearch()
}

// const addOrEdit = async (e) => {
//     try {
//         e.preventDefault();
//     } catch (error) {

//     }

//     console.log('submitted')
//     console.log(document.querySelector(".editMovie form"))
//     console.log(new FormData($(".editMovie form")[0]))
//     values = new FormData($(".editMovie")[0])
//     const data = new URLSearchParams(values);
//     console.log('doc id', values.get('id'))

//     //Empty Values if present in Modal
//     $('.editMovie input[name="id"').val('')
//     $('.editMovie input[name="name"').val('')
//     $('.editMovie input[name="director"').val('')
//     $('.editMovie input[name="genre"').val('')
//     $('.editMovie input[name="99popularity"').val('')
//     $('.editMovie input[name="imdb_score"').val('')

//     let options
//     if (values.get('id')) {
//         options = {
//             method: 'POST',
//             mode: 'no-cors',
//             body: data
//         }
//     }
//     else {
//         options = {
//             method: 'PUT',
//             // mode: 'no-cors',
//             body: data
//         }
//     }

//     const response = await fetch('/editMovie', options);
//     // const moviesData = await response.json()
// }

const submitSearch = async (e) => {
    try {
        e.preventDefault();
    } catch (error) {
    }
    console.log('submitted')
    console.log(document.querySelector(".advanced-search form"))
    console.log(new FormData($(".advanced-search form")[0]))
    values = new FormData($(".advanced-search")[0])
    const data = new URLSearchParams(values);

    const options = {
        method: 'POST',
        mode: 'no-cors',
        body: data
    }
    const response = await fetch('/search', options);
    const moviesData = await response.json()
    let columnsToHide = [0] //Hide Document ID Column
    console.log(moviesData)
    if (!moviesData['admin']) {
        columnsToHide.push(6) //Operations Column
    }

    if ($.fn.dataTable.isDataTable('#movies')) {
        console.log('table exists')
        table = $('#movies').DataTable();
        table.clear();
        table.rows.add(moviesData['data']).draw();
    }
    else {
        console.log('new table')
        moviesTable = $('#movies').DataTable({
            retrieve: true,
            data: moviesData['data'],
            columns: [
                { data: '_id' }, //unique document id, not to be shown
                { data: 'name' },
                { data: 'director' },
                { data: 'genre' },
                { data: '99popularity' },
                { data: 'imdb_score' },
                {
                    mRender: function (data, type, row) {
                        return `<a class="table-edit" data-id="${row[0]}" data-toggle="modal" data-target="#edit">EDIT</a> <a href="javascript:deleteRecord('${row['_id']}')">DELETE</a>`
                    }
                }
            ],
            "columnDefs": [
                { "aTargets": columnsToHide, "sClass": "hidden" },    //unique document id is stored but not shown
            ]
        });
    }
}


$(document).ready(function () {
    //Fetch Genre List and Load in DOM
    fetchGenreList()

    // Loads Selected Row Data in the Modal
    $(document).on('shown.bs.modal', '#edit', function (event) {
        var triggerElement = $(event.relatedTarget); // Anchor Tag that triggered
        var tds = triggerElement.closest("tr").children("td");

        //Set Values of Selected Movie in Modal
        $('.editMovie input[name="id"').val($(tds)[0].innerHTML)
        $('.editMovie input[name="name"').val($(tds)[1].innerHTML)
        $('.editMovie input[name="director"').val($(tds)[2].innerHTML)
        $('.editMovie input[name="genre"').val($(tds)[3].innerHTML)
        $('.editMovie input[name="99popularity"').val($(tds)[4].innerHTML)
        $('.editMovie input[name="imdb_score"').val($(tds)[5].innerHTML)
    });
});
