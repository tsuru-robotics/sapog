# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/reg/drone/service/battery/_.0.1.uavcan
#
# Generated at:  2021-09-29 15:15:52.710421 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     reg.drone.service.battery._
# Version:       0.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class __0_1(_dsdl_.CompositeObject):
    """
    Generated property settings use relaxed type signatures, accepting a large variety of
    possible representations of the value, which are automatically converted to a well-defined
    internal representation. When accessing a property, this strict well-defined internal
    representation is always returned. The implicit strictification enables more precise static
    type analysis.

    The value returned by the __repr__() method may be invariant to some of the field values,
    and its format is not guaranteed to be stable. Therefore, the returned string representation
    can be used only for displaying purposes; any kind of automation build on top of that will
    be fragile and prone to mismaintenance.
    """
    def __init__(self) -> None:
        """
        reg.drone.service.battery._.0.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        """
        pass

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: __0_1._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        assert 0 <= (_ser_.current_bit_length - _base_offset_) <= 0, \
            'Bad serialization of reg.drone.service.battery._.0.1'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: __0_1._DeserializerTypeVar_) -> __0_1:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        self = __0_1(
                )
        _des_.pad_to_alignment(8)
        assert 0 <= (_des_.consumed_bit_length - _base_offset_) <= 0, \
            'Bad deserialization of reg.drone.service.battery._.0.1'
        assert isinstance(self, __0_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
        ])
        return f'reg.drone.service.battery._.0.1({_o_0_})'

    _EXTENT_BYTES_ = 0

    _MODEL_: _pydsdl_.DelimitedType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8D1%gC0{@j)|8E>e6?a9U;gSMTXbKdmqo5*3ve!vf5Gvw_BsL{DbuHUPR47`_?!LPjyt}iVnLYa=1<@ZsL^_E|UH%~cGd^#2'
        '_PlpVRAIHs-ObGV@_C>4c{6{1^FKQ`x5D4@{bo_PqD)dpR?AX9lUYegnwzRIPJ8N>Z|_s7D|{@@77caZba%h%o_E{J@1?q~$#!aM'
        '`Sz)|ZSGr3>s!8?*0O?$_bknl!kU^AxS8vml1zF}c9Epr@>)74>$Iua)LVawpTFr2w+`R<XZKaNyq;pS)miJwbx*tHt<m>1Tl7wz'
        '^S*)_OSwd>-HYW9(y6|rB5jQIsV=&s<;~QY*5-tTlF~+c)h)9<Up0FRdEWY6Mq>9_Re$v1{9d`&v{|Y16tTA@n@kJoW$KZk+pVNS'
        '_<LB}3wiCuy!K*Vduehnxu3Lhp39meR?@+trP`-)D<XU|Ell41`M)=|w$7Ax0{?kM!d23G5iN<z)Y==X>zNq96Aw1_;Gm^1TWzTj'
        '-iQ#nQ^DBOl%=@{r`znWlzaE_WFo}r=MVpQ@aRlz{+)esd?5ahKkQG$$%C^4@s~e5dkVt@PRte&=+VY23N&irbnX%=5slTk_KV~+'
        'Y(H~X`|l@7a{t~vSd2-g&P(6AS6SR7)#=90{_k)1N5)VKum&I9w;4O$*cpx8OFo=TKFfGF0ch!ksmnzVxwg&^a0?JXWF%UL+DwfV'
        '<h-t==Zf%Vs*Bdj8d#ZW_@OZuWJQl(BF^xO!OwP8z6n?)3UYc@M~hbs*%5`7v)aH#?skN%3sFg3d#c$(f`A*3=8|Q(*a^-C0>z|5'
        'uyEvZv==dzB#@DXuE{x(o7!7bt}@$pM6Uo2+JT6Yli}RmoympLxk9QeE^dRC{=x_o!-D@tX1df~Q_s^~ar)%o;21d;^s%^5REOhN'
        'L9JkhSL7Qzs3d9x6Nc9F#1=WD3T-Id0xewOmjwdDqL33VETW1fK)SB2LS%y}Xrj{@%3P4ly`J}FbfyZ`)84Hmki-Pe9vtmI{353C'
        '?a}C}Df=H~QRoPalT-2w(OBb=Eq-%7>G(k4$Axwj65w*%DS;#x+V>hz8(YDKX~@cuPNdqLP#4I(_&xLTQnKS7FK=b=G75De!Wan4'
        'mAuqdTSdTRA@bJR5HT3X8z98+4L5~$xsrB<2B=G}7q7-zfxZD(mal`OPab@7u%C#B0N3=Wu9ptf4E`bnj5d|il}Fb$O{rm0>6zM{'
        'o6-YXvHwWa1cupjF}0==GS78^K!HXfE8YQWmNZ6#qk%e{Q;`IJPdMwLTTSbm)<=Q>w5#+Yq%Q-9aJ(qNS8gZFCQJ@%8n_AsgK866'
        '6WZTrhyIgc5)a|*2*n$aA37+qAXk*1JHbK#n`l&o!L3z5gK}C!O}i1=poR&n5$)hHlmJwHJRNscsEZ2{&Dp?AZF~S3)0B$Mu3E(9'
        'k#elJ>4tXfOmr=JRmi0S<~XcOTNVNwMYJdpy37)L3w_lGBv(Wk(`l4zTTfw%MG<-{wkeq<(8QJ|2&kZ$mBp$7q?k%w;?8mx$%A!>'
        'a1OUv4SkN9&j&Hyj`Y4OrjQ5MQ;9u~=(WOjm>VqJmJmv8si8%*o76Ou!Td_kh7^Los9`}7dJ$j66AoxLg0eFyd-j2<lhd$2%0fxF'
        'Q!%}(w)7fpedR$ib)4n};A~n4pd<Dfw<ZvrwXe8H#PJK{pnYn>c0f14=!l0Y)1|L1Vma>5!N`}b1g5NpBPRfHw~?qG?qLY3_a)~>'
        '7XnvM={PZ(PI=lTD_eGD0S&}h;EW5Bg+rwn4Rq;ErE?x~2<0r$uxIT!8g8Dc$-`JSeGz13S`>&g440T5$~eDquPmjmc;pV%Usd`s'
        'V3;`8Z9QcPnrph?qI2{0r!gsOX7B6WVDBA=DNe;5aA|D+w?csxsAq3-5(FOiTrbyJldn?TG`RuKppO|Y!rTPwE^*9inzLFA?zwxj'
        'AlbN!FhgOKF5v@nXEKGH8HS$aCnf-zg-HUI46-+{3ysHL$1@=j2fd%+;?u_r-WGw|@#2bmO^y@HBOa6`b08Y;dw<>2PE?N=ysqMC'
        '4zwstn0<zo8dzx8>+*TD8TcC-Cv?yvjKF<z4IVked_pPn5UY!Y3_@BvOpnM{c$F-OP-|o@8_Xria)z@qZW(4B-wY>#X|fEs4!vw?'
        'l;Ao(8{8Z&%dz2i*2-H3OqgrTgm~GU6q<R!cT&SJ6rjheZ=Ai-#9l!UDO0!+Jx6hI)2yy1;iuh#rcn4I>F}D#O4luaIlL${?bDL#'
        'nOAu7_|5O#^2S5$pM>wH_!=LL%kQM7>6YSkM%<#x3~GZn)u&V$yjMAj&jKHf9luU<4ECZ^zgYh8nD0^b?4?a=n^%w8vXpkQxe5z&'
        'S+>;uyW2k8`r2i9r#8Kz?(kZhA>B&Xc%<?NdC4E%O2J&b75VferOQUv;VFBBv6!`)nyBmQhWe4Z`Lt8Fo_Fe<7wYzrdRP5K{q%+U'
        'nR*WfxbJGu#%`xYe0SSaVT|G*etLGVd$Bh*+*9V*aqIKCe;quAQq0J%KgzF<FzpTnBE<yu96ELCcgx$ygCRbaJi^+iyoC4o8~^A|'
        'y5*1gAyyY?-?5>8A-|ui_k$00M}06t_?<_%l}LVrysA{o@As90RN!sDt&-lveTH2C_BB)Qp2&JeCr~P{Usw0@SPr#r>)O|$1|MPJ'
        'SNQ+e&r!u#TJ;-Lh#W5pEQ*&G`DpS#dG{4sHxU2;'
    )
    assert isinstance(_MODEL_, _pydsdl_.DelimitedType)
