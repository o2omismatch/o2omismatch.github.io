// helperfunctions//
function percentNumber(num) {
    num=num*100
    return num.toFixed(2)+'%'

}

function percentNumvisit(num) {
    num=(Math.log(num+1))/13.4*100
  return num.toFixed(2)+'%'
}

function percentNumpre(num) {
    if (num>13.4){
        num=100;
    }else{
        num =(num)/13.4*100
    }
  return num.toFixed(2)+'%'
}
function svgbar1(num){
    width =(Math.log(num+1))/13.4*120
    return '<svg width="150px" height="12px"><rect x="2" y="1.7" width="'+width+'" rx="4.5" height="9.5" style="fill:#c22e01;"/></svg>'
}

function svgbar2(num){
    if (num>13.4){
        width=120;
    }else{
        width =(num)/13.4*120
    }

    return '<svg width="150px" height="12px"><rect x="2" y="1.7" width="'+width+'" height="9.5" rx="4.5" style="fill:#00939c;"/></svg>'
}
