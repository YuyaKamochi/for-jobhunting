'use strict';
/*
L.Iconを渡すとアイコン付きのL.CircleMarkerが返ってくる。
*/
class Icon2CircleMarker{
  constructor(){
    //既存クラスのメソッド上書き
    this.icon2Canvas = L.CircleMarker.extend({
      _containsPoint: function(makerPoint) {
        //L.IconのoffsetをCircleMarkerへ適用
        const offset = this.options.icon.options.pointOffset;
        if(offset){
          return L.CircleMarker.prototype._containsPoint.call(this, makerPoint.subtract([offset.x, offset.y]));
        }
      },
      
      _updatePath() {
        const op = this.options.icon.options;
        if(op.element){
          const ctx = this._renderer._ctx,
            p = this._point.round();
          p.x += op.offset[0];
          p.y += op.offset[1];
          //Canvasへ描画開始
          ctx.save();
          ctx.translate(p.x, p.y);
          //アイコンの回転を適用
          if(op.angle){
            ctx.rotate(op.angle * 0.0174);//Math.PI / 180;  
          }
          const x = op.iconSize[0],
            y = op.iconSize[1];
          //drawImageでは描画位置は整数にすること (https://developer.mozilla.org/ja/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas)
          ctx.drawImage(op.element, -Math.floor(x/2), -Math.floor(y/2), Math.floor(x), Math.floor(y));
          //文字は前面に出すため、drawImageの後に追加
          if(op.string){
            const count = op.string.length;
            //文字を中央にするため苦戦（アイコン、フォントによって変わるため適宜変更のこと）
            const fontsize = (x/count < x/2)
              ? (x/count) +4
              : x/2;
            ctx.font = fontsize + 'px sans serif';
            const offset = Math.floor(count * fontsize*1.3 /4);
            ctx.fillStyle = op.fontcolor;
            ctx.fillText(op.string,-offset,0);
          }
          ctx.restore();
        }else{
          const element = document.createElement('img');
          //element.onload = () => this.redraw();//redrawしないと画像が切れることがあるが、パフォーマンス優先
          element.src = op.iconUrl;//キャッシュが効かないと重いため、なるべく同一画像を
          op.element = element;
        }
      },
    });
  }

  getMarker(latlng, options){
    const op = options.icon.options;
    op.offset = [op.iconSize[0] / 2 - op.iconAnchor[0], op.iconSize[1] / 2 - op.iconAnchor[1]];
    op.popupAnchor = [0, 0];
    return new this.icon2Canvas(latlng, options);  
  }
}

