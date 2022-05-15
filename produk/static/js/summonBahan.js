// $(document).ready(function() {
//     var sum = 1;
//     document.getElementById("add").onclick = function(daftar_produk) {
//         sum++;
//         var bahan = '<label class="label" id="bahan'+sum+'" name="bahan'+sum+'">Bahan:</label> <br>'+
//                     '<select class="form-control" id="bahan'+sum+
//                                                 '" name="bahan'+sum+'">{%for row in daftar_produk %}'+
//                         '<option value="{{row.nama}}"> {{row.nama}}</option>'+
//                         '{% endfor %} </select>';
//         var jumlah = '<label class="label"id="jumlah'+sum+'" name="jumlah'+sum+'">Bahan:</label> <br>'+
//                     '<input type="number" id="jumlah'+sum+'" name="jumlah'+sum+'">';
        
//         var newContentBahan = document.createElement('div');
//         newContentBahan.innerHTML = bahan
//         document.getElementById('target').appendChild(newContentBahan);
//         var newContentJumlah = document.createElement('div');
//         newContentJumlah.innerHTML = jumlah
//         document.getElementById('target').appendChild(newContentJumlah);    
//     }

    
//     function removeLastElem() {
//       sum-=1;
//       document.getElementById('target').lastChild.remove()
//       document.getElementById('target').lastChild.remove()
//     }
// });
