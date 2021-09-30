# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/node/435.ExecuteCommand.1.1.uavcan
#
# Generated at:  2021-09-29 15:16:17.797345 UTC
# Is deprecated: no
# Fixed port ID: 435
# Full name:     uavcan.node.ExecuteCommand
# Version:       1.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class ExecuteCommand_1_1(_dsdl_.FixedPortServiceObject):
    # noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
    class Request(_dsdl_.CompositeObject):
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
        COMMAND_RESTART:                 int = 65535
        COMMAND_POWER_OFF:               int = 65534
        COMMAND_BEGIN_SOFTWARE_UPDATE:   int = 65533
        COMMAND_FACTORY_RESET:           int = 65532
        COMMAND_EMERGENCY_STOP:          int = 65531
        COMMAND_STORE_PERSISTENT_STATES: int = 65530

        def __init__(self,
                     command:   _ty_.Optional[_ty_.Union[int, _np_.uint16]] = None,
                     parameter: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]] = None) -> None:
            """
            uavcan.node.ExecuteCommand.Request.1.1
            Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
            :param command:   saturated uint16 command
            :param parameter: saturated uint8[<=255] parameter
            """
            self._command:   int
            self._parameter: _np_.ndarray

            self.command = command if command is not None else 0

            if parameter is None:
                self.parameter = _np_.array([], _np_.uint8)
            else:
                parameter = parameter.encode() if isinstance(parameter, str) else parameter  # Implicit string encoding
                if isinstance(parameter, (bytes, bytearray)) and len(parameter) <= 255:
                    # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                    # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                    self._parameter = _np_.frombuffer(parameter, _np_.uint8)
                elif isinstance(parameter, _np_.ndarray) and parameter.dtype == _np_.uint8 and parameter.ndim == 1 and parameter.size <= 255:
                    # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                    self._parameter = parameter
                else:
                    # Last resort, slow construction of a new array. New memory may be allocated.
                    parameter = _np_.array(parameter, _np_.uint8).flatten()
                    if not parameter.size <= 255:  # Length cannot be checked before casting and flattening
                        raise ValueError(f'parameter: invalid array length: not {parameter.size} <= 255')
                    self._parameter = parameter
                assert isinstance(self._parameter, _np_.ndarray)
                assert self._parameter.dtype == _np_.uint8
                assert self._parameter.ndim == 1
                assert len(self._parameter) <= 255

        @property
        def command(self) -> int:
            """
            saturated uint16 command
            The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
            """
            return self._command

        @command.setter
        def command(self, x: _ty_.Union[int, _np_.uint16]) -> None:
            """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
            x = int(x)
            if 0 <= x <= 65535:
                self._command = x
            else:
                raise ValueError(f'command: value {x} is not in [0, 65535]')

        @property
        def parameter(self) -> _np_.ndarray:
            """
            saturated uint8[<=255] parameter
            DSDL does not support strings natively yet. To interpret this array as a string,
            use tobytes() to convert the NumPy array to bytes, and then decode() to convert bytes to string:
            .parameter.tobytes().decode()
            When assigning a string to this property, no manual conversion is necessary (it will happen automatically).
            The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
            """
            return self._parameter

        @parameter.setter
        def parameter(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]) -> None:
            x = x.encode() if isinstance(x, str) else x  # Implicit string encoding
            if isinstance(x, (bytes, bytearray)) and len(x) <= 255:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._parameter = _np_.frombuffer(x, _np_.uint8)
            elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size <= 255:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._parameter = x
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                x = _np_.array(x, _np_.uint8).flatten()
                if not x.size <= 255:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'parameter: invalid array length: not {x.size} <= 255')
                self._parameter = x
            assert isinstance(self._parameter, _np_.ndarray)
            assert self._parameter.dtype == _np_.uint8
            assert self._parameter.ndim == 1
            assert len(self._parameter) <= 255

        # noinspection PyProtectedMember
        def _serialize_(self, _ser_: ExecuteCommand_1_1.Request._SerializerTypeVar_) -> None:
            assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
            _base_offset_ = _ser_.current_bit_length
            _ser_.add_aligned_u16(max(min(self.command, 65535), 0))
            # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
            assert len(self.parameter) <= 255, 'self.parameter: saturated uint8[<=255]'
            _ser_.add_aligned_u8(len(self.parameter))
            _ser_.add_aligned_array_of_standard_bit_length_primitives(self.parameter)
            _ser_.pad_to_alignment(8)
            assert 24 <= (_ser_.current_bit_length - _base_offset_) <= 2064, \
                'Bad serialization of uavcan.node.ExecuteCommand.Request.1.1'

        # noinspection PyProtectedMember
        @staticmethod
        def _deserialize_(_des_: ExecuteCommand_1_1.Request._DeserializerTypeVar_) -> ExecuteCommand_1_1.Request:
            assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
            _base_offset_ = _des_.consumed_bit_length
            # Temporary _f0_ holds the value of "command"
            _f0_ = _des_.fetch_aligned_u16()
            # Temporary _f1_ holds the value of "parameter"
            # Length field byte-aligned: True; all elements byte-aligned: True.
            _len0_ = _des_.fetch_aligned_u8()
            assert _len0_ >= 0
            if _len0_ > 255:
                raise _des_.FormatError(f'Variable array length prefix {_len0_} > 255')
            _f1_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, _len0_)
            assert len(_f1_) <= 255, 'saturated uint8[<=255]'
            self = ExecuteCommand_1_1.Request(
                command=_f0_,
                parameter=_f1_)
            _des_.pad_to_alignment(8)
            assert 24 <= (_des_.consumed_bit_length - _base_offset_) <= 2064, \
                'Bad deserialization of uavcan.node.ExecuteCommand.Request.1.1'
            assert isinstance(self, ExecuteCommand_1_1.Request)
            return self

        def __repr__(self) -> str:
            _o_0_ = ', '.join([
                'command=%s' % self.command,
                'parameter=%s' % repr(bytes(self.parameter))[1:],
            ])
            return f'uavcan.node.ExecuteCommand.Request.1.1({_o_0_})'

        _FIXED_PORT_ID_ = 435
        _EXTENT_BYTES_ = 300

        _MODEL_: _pydsdl_.DelimitedType = _dsdl_.CompositeObject._restore_constant_(
            'ABzY8L4#Cb0{@j+O>ZQ{8TKZ?dV3)(*|3lxLS>VHE!pG1vJhpZL|%Igmhp$iUN!_!Q`22DRoR}dp{v^Vtda;0L?E@4RcKBq%8f&A'
            'D4(ZXa?T}xCb=cgTh-k&V~+#N3T;n!eY_vf^Sp1>zW2Z<-+F4!{Z~9Q9K|M1TA>k{;)%M;yNPIpksb`SQC5`2BkLkj13bnDqoF82'
            'E*IY~e_1XR4}~gCMOMnW;*ouu<&n)ZF+JqLFy#X*aW&_M5l>sGjzz0|ETY_sH9Z*cG;VdoySXs7Eat;Qkr|~^TJikr)$_;Y*14^7'
            'zb@Y|i;E$*Hd9?pHs#w`{tVljQDyPqh7w6UHYf;VZh2_Q%Cn{qGxAm)V#MWJsZsq@#G9!VeUVLjcQNcL8zv&{TUl;h!r~D(HXOjo'
            'Qhu|zvR5xe(^_lzwoRYl(cA}Rr!2k^8jA?<ES_BG!@Mhl;(X-8Qx*?|v5v~(-}}{AHq69wEP4uNv1*iIJQIvtW~E?O51H<{$Bd_a'
            '!4~S#U6JUc#a8gTNMoHDhLkY>4fA0_#<S59J9J-{%}_+Dr=sy5Ds_u?wY7S{hCH(;_JKQ@RcW8~G7PvYGTm%8V>u&vlCV@;mK(uT'
            'EK-XBNIT<QeJI$q7hZnp<yMJsJnjQ7pDdm_BjZ`dM`iKE>l|<K<~0|}ReC#}vPVLZhyix;5Rgw*D}Q@yUOpqgE5C>67Z;GnA&-<D'
            'm0SNUzFs9J>=Be^&il^RIZCLX{Xp1FOj$fzTRKiHjJ79#m&L<3mG$=S<7Z`Q@zqcd%YvP?h#3vKI#IyI<!v$0h=T=Lc84P4R%eqO'
            'jidqr<WGvn*K`_jE7F-m$!QvyiIk{?@sIB0NdiEe8u?Io$dg=@zbO~C=I@!VT&;q!j#*E12nroB6jq&O(w%U?j}cl-c+I_(yY*Tw'
            'egl<)BJ_Y^+y6OVoF`7@38(p6=V<KQy{&owcMjT#;~`I-TI}Rq0gK*5THe~8o0o6Tnjtxc(O%%$1;7{*Wl6`LE&jF24739XZeBB!'
            '4~K~Yd#rX?ukhPq2l&y`*#NY|Z?FTS!A<Mp%ao}{HqdVcG^OVJm<X|MSYRdQIiRrx2#*G<m0et7;y4mRM=k4iO+aM)`cc5xGF#i-'
            '-d^2V4{x?#+1v^DcQ+1huXftut-bZtgEsN!axstO)5Z<JK&A;0UuwXQkUUzi*J<w`tac74Fz<ClS8J~?PQ-&9ZOL3XZ}ec6R|7s`'
            'I&*)KcNt_}kx1dm=>*A%&SFHE0?Y3RCVD*)*&9r>`mH6_;}LK(qTxV1Fj72SvjO?WTT1wpTF-Y}=y_5*i8&W~8P>sDP;!2wddBzS'
            '!I!RIzjnPO-a07AFAB?Jby)UxZ?`+)?#2cM=4bmdx5(g8+QjAt>*X1KWQ<1<%w$KZ(z&i+D5^$5p;!*JOWd5HKEhb!9re?xG>`5u'
            'xCZm(yOkgE&>Q^XeHi@o|Hp-V_NTuK=H_mSex>V1_v{hXk$i|E3A-}w%+C$suBzZY1-<PE?(jdxIMRGa7zg31BwTG6bhQGst3I9s'
            'V|GP4wOpmfM}k{f(<~K7V~f;)qrTAI^ci8KfG3*A6t0oCUSwz=eC2U81!q$mc;oFP?`Wio#0-yiyKWT^Yez-x<cs)hj`+}9ndt<s'
            'R&M%jNC1Md6|Eq+HN>1uIM(9HjUI<<Y0~5cA8)bffg(s<DgH-NI20*M;Anv30#M~FI3s5*w%PMuU}h{(@t{wGdWoe;9rK$aq?!0R'
            '*eB=(vY^vClYz)GO^J$yVRa`_K?W>@pN3qCru=l{TmfJUp3XN{*F(t3L7S;wLlvizd4{56lTo14<v6z^r=}db8>1!gvYO>h7?nkT'
            'fXxoEIt+3#h4w>7U{;<Q-h+R%g3)jS{Rbj}Hs=JUF^wk~l0L#5%st{GAC)Q>Xijtv%%T&?yz136Y3W+QT%>BS5{{OFJWXiS<Wj!N'
            'f)@j7v?^?22VWInwZpaYlMHxK0li9JZD&^ylE=Vb3Xp^&sUnFTsDY|RgJix~`Q*fG|JK@Cdw<_qPIOagF5F%k4xYeG;BX^Ir!z_s'
            '(++}|7Q1X3>OP|+k84(CzIzw-O4Ctv*g{E!upy%ph6D~B+<HU2zi1*&51ZAI2C-FosPBAf0%ND4z?yL~nvhre98h$t^$90Ev^FEQ'
            'FiZqRE)%_~3Q1CyD5nO|vmW)`CxVU*jCw!!YTycU>Z?DE15Qu|2%EWqQ~`FuZRxW(A*`^%XVJ$eo(VZrJGT%WBiMrXfaLQky|_xu'
            'n><XtDgeYTyj~38!1nHX`=rpf*xr|NbLOfuy@hj|4s3ve?x*T5;f;bc&<5?m2yhrwRZsFmr&tY(X>*kUSy(HnGihiDl$LgwRf>Xz'
            'idL@GaHF6E%^-==O7c9U(84Szop16f!rau<@+?XHB2x9`GC$-h;a!!W)vxWQ)NQK>7z9-y^$8tFoOiU<81AsR;*R&Ir?P>w#x*>`'
            'k1%u=6Yjj*s3Q%oG_RQyIKgt7LY9g_SH!Niq33dJN0s1-1wi_;q9okSG>@e4XTPRAz~3X0B#S5kskfW_UJ8yHIL=y~l9{I|0_ZX6'
            'zy~@({V?!QasL)Mph7$wDiwaaBA5k3GAz+Z5I5B+^2FwDZ*fSH-y`Mm(Ou3&LR6X1{DAyzsz#&VEw%xyiepaMU#hFj3El4@;j~y9'
            'pELpvQHw^urXaW!G_vf1GSjzl4fPRgRRrOQ(Wh9VNDBwk5F^&xCi<LC9FeD{Z?UOUh$kJYfH-Cu(SOLNN>39zv|8K=*n-JXE~*Sr'
            '`j$7>>rSTXM(WTsc%JCJs6Sf-u7fjR<j+KwQWaGl5*0fVUf*~#bW03MN%gwfH$s!uG!FGy$qUV_7WmqIw7`$oE%3(b+QDw;4LZ`a'
            '-GSyG9bc8|Ks@LAh@R@_Rln!D@JcM}qX@bho+q|WmSGD-_WEQ~bp;TR^<30b^E46}b+}NNx}lpm0-1U?l&UXMk*UaQCAJi%=|U3V'
            '+mP@@69=f7(RtxMqI0E=PJ6rEd8NIx_69n%-8~A=Z`WMOm~6BLXd<a%C+L(&TgeaVwn(>ZeV(aIBL-|#hoEr_?T>;^1@Qj#VQ3te'
            'x;I69yn156S>8T>AKpGwdkY`I+`V>Ze{=t!y>sB((tSD*t$k%~Zt7TrlZm_895bep^~`H&E#%YK86R)lO^I(By=)KZS`!5Xb6ng^'
            'P@i|u{T^!Ym54?gfORdl<GOBlxi@a?U>Q;J)KZM+R#S<NFc?|VT?lt`Y2a!SAQVg<M5xK4N96!bn=mI4zTKH&*+2}42~#_fprnHI'
            'm1mIQS79fVWXToUAax#4>J!H(cfkQx_>(#c?-HBtW8H{}>zBH!(BTqiv{$}>C4uW1#nf?Y>Z(DcCeJ4NaOWy14<$8jDo~T}SPPRr'
            'XUAQ|*!iGIK_sfI(14jx{Xqj&QCyz5$PT+Be@RY|{l2^+g<OyWspPNZUHOsxK$h~J{Js2C{y~107Z<}=PzO%3UVc=3E$pdd5r<TD'
            'LKT-g#bcq-Ib<Rv!465V%i<R+5}8;rDnVLS?&e*7ykhuJ_g89>U$I&zW(DRD3_@SuSB7~PWhl%<KX-Lxe0OeEsv#7il^3sFKY6MD'
            'JpTA0CA^i~z!V}%Sap2mhY*?1H>cQD6`-1A74exndqR9D##5~n<j3WNjwC1U!&|{BA^Fsu6cI@eJ@jrc)e<<EQq}M0z#9PN`30=e'
            'rJwJ8KoEaT4HzS_Ka@9oVt+h!?fK{)kLgTw>betO$Ky8q)J?iz9l!m1^E7!Idg-3&7V`+3TesXgm(#W8CHWTqe;b474pZLrmz___'
            'x3(|Mk6-_DYd)Xx-d}mji}GQ4Nj^qKTmjY;aP|Q(_Nn|#$j`qF3gsU^l7HHff0lode?=bU--`30I3^(~x8J!?TmeS?KNw}96x0`-'
            'x-@4H=9j%N&kX2fpeBRDrmve1s;ArAOXp@@Cd)T>5Q29uPzdVlU*lro0!JU;oAHsRw*Cjr?J6K88vp<'
        )
        assert isinstance(_MODEL_, _pydsdl_.DelimitedType)

    # noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
    class Response(_dsdl_.CompositeObject):
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
        STATUS_SUCCESS:        int = 0
        STATUS_FAILURE:        int = 1
        STATUS_NOT_AUTHORIZED: int = 2
        STATUS_BAD_COMMAND:    int = 3
        STATUS_BAD_PARAMETER:  int = 4
        STATUS_BAD_STATE:      int = 5
        STATUS_INTERNAL_ERROR: int = 6

        def __init__(self,
                     status: _ty_.Optional[_ty_.Union[int, _np_.uint8]] = None) -> None:
            """
            uavcan.node.ExecuteCommand.Response.1.1
            Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
            :param status: saturated uint8 status
            """
            self._status: int

            self.status = status if status is not None else 0

        @property
        def status(self) -> int:
            """
            saturated uint8 status
            The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
            """
            return self._status

        @status.setter
        def status(self, x: _ty_.Union[int, _np_.uint8]) -> None:
            """Raises ValueError if the value is outside of the permitted range, regardless of the cast mode."""
            x = int(x)
            if 0 <= x <= 255:
                self._status = x
            else:
                raise ValueError(f'status: value {x} is not in [0, 255]')

        # noinspection PyProtectedMember
        def _serialize_(self, _ser_: ExecuteCommand_1_1.Response._SerializerTypeVar_) -> None:
            assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
            _base_offset_ = _ser_.current_bit_length
            _ser_.add_aligned_u8(max(min(self.status, 255), 0))
            _ser_.pad_to_alignment(8)
            assert 8 <= (_ser_.current_bit_length - _base_offset_) <= 8, \
                'Bad serialization of uavcan.node.ExecuteCommand.Response.1.1'

        # noinspection PyProtectedMember
        @staticmethod
        def _deserialize_(_des_: ExecuteCommand_1_1.Response._DeserializerTypeVar_) -> ExecuteCommand_1_1.Response:
            assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
            _base_offset_ = _des_.consumed_bit_length
            # Temporary _f2_ holds the value of "status"
            _f2_ = _des_.fetch_aligned_u8()
            self = ExecuteCommand_1_1.Response(
                status=_f2_)
            _des_.pad_to_alignment(8)
            assert 8 <= (_des_.consumed_bit_length - _base_offset_) <= 8, \
                'Bad deserialization of uavcan.node.ExecuteCommand.Response.1.1'
            assert isinstance(self, ExecuteCommand_1_1.Response)
            return self

        def __repr__(self) -> str:
            _o_0_ = ', '.join([
                'status=%s' % self.status,
            ])
            return f'uavcan.node.ExecuteCommand.Response.1.1({_o_0_})'

        _FIXED_PORT_ID_ = 435
        _EXTENT_BYTES_ = 48

        _MODEL_: _pydsdl_.DelimitedType = _dsdl_.CompositeObject._restore_constant_(
            'ABzY8L4#Cb0{@*>>u(cB5KmMdCOira(3e`SqD8<5J2X&LYNggV4vkD4WIKGQ6s`8|CY}}NyX!vkK&6GYAdt2Km94~=KKM^Nd*>vM'
            'Arh(m!FxBmv%mSxZ)SY|z@I-KnJ7N?T)r8rIH@uPQt(9F<zWI<7G;AxQ$mBY$LAms16szt%^ciwcj<w<=PueqOr$ADhZFXAS4$IV'
            'BVqTJgDm9(a&g}9wTP$HG>f6y+<?evXk>!{PvdF_RGy`Zc2(FKNF}n=yF7e*xPI<hldZ`|?t!yM8P{5hkWMSNLjLyvzrD-ZgYyEC'
            'cn8rGi@D}ZdzgD2&!rDntkI6?<y47&3h_d!p$~F*ct=?%G)o}uYjmv&Ighx~Y(P;ueBYkEwdKekt2W5C=uH&S#6#C{_B2zPDBv<4'
            'b@bSTIAsr!NgL(t0TySGvmf*j0tw0_I>=T7T|E6@K<TQZ1JkzBAQs7;-o}UT;fKT3$E^yU!}IuQ>HI{uSMM!%S$Db7Xm+~}FW8`~'
            'xuhHinGB%JP#h=|MWEEGNs>)R318!hAyz)x;te)(g5=Y*i?vFJYkJ3%Ehso+kE}`_`L`5OWq!COyPceIo(vTdvP*9Ye7?SLbGg&>'
            'z`tr_CW(VI(}D6K_y9aRF(@H@JVuk4A&9oOg`PSdA;bg>XNL&!OFMaGA5hK=p|qEJtiIg)ZmF~IeRIwuIzI=gpqpa@fzE=2M|XV6'
            'xY3wN5?K-X*v+5s<K}mUH(#&MvBuKkV!d5lJKNjQ1l=B$^%V$J1brvX)>F?-L6ph!%x8NX#_T>|oF0L3tKO+EHhayE2l9;v;;%?N'
            '3ptn612o8hI>3;AqsXu>G!~gskU%s7c^uT$eSkVS0?IE7iQMpjA|oZFg-A4Pm5^^pL7YL!Q4W$MJd{5rsoX^b?g8xD|B%Z<n^<bs'
            'Z?a~mvsBPE@6ly+cOi^GVIfrHYf#o7#6%5svw)|8NvY&YvR1iBsNn`#R7Ca)xG%QBft?;{oGjcdyRrxQ8J@)|UdC_nYi!{Syp0{?'
            'xPl2HuA?&4;$om0kGL1h6MKTKiVcXFR}T}hYui&yWkyCoh6Gs7se#!aYe*GWQzD^;Ub|~TzEM*=&-%4hAqVSRLQQ8`qG|+3i?q+m'
            '@leZ6n23l;=$ph}xYMguZMelJtaf$w+V~W?Lf>)=HEo7m5fq<p-`dwi1nx00J>k1)m{140u+_nK`Y!F%<Im0>yDs$2;<*dkoz=d@'
            'vfSBVFDGhq5M~q!L0N=BHZ1w2BE^{;ouCm4nojt;eft)VW1`}fP56hmwy6VixjAmdnWyeztMW{RG(7Xt0}Ub*Qk(;k`k6!vzTp>#'
            '{ahkmJ^m@*xp`X5*R}}@1yA8oJccLn6b)8V#br{&4N}7jDM11L^d@S-`%mye8-KxH@i*cdAJV0;p(zb+@&2SeOIj-bNl1pkWBMuP'
            '@JPu7R5G8mCcSdY!g+*G%1A9f9U<fl4Lh&N^tH^|BPFpU0RJ}uUyP6y5Lvriz1!hwA3BhO7JH@XPD$bn9e6QDJYoE+jek>o_|HA!'
            '*}tE7rtl^43TkNl_cca;wE7<g1_cL-2><{'
        )
        assert isinstance(_MODEL_, _pydsdl_.DelimitedType)

    def __repr__(self) -> str:
        return 'uavcan.node.ExecuteCommand.1.1()'


    _FIXED_PORT_ID_ = 435
    _MODEL_: _pydsdl_.ServiceType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{^vI+ix7z8Mi4AXSgI>5>OD$QBr{e_8JHQwP{rxdmSvtcDmj`L9HfdXU_UeGCOBG7u%b*YEab*(5OXac<4hV9{R>Z'
        'RaL5bed0ghsr@(l(DG2V{e9=0nVns)1Fi&!@$AgGe3#$%`@ZiCx9|So{Fy2JPky>T@Do35xQU1Z9tO8~Cln3WQ@y@Qf>adweOn^l'
        '2|Upr^hNQ0aqg|+hsA9EfE$bNWg<!4l%C6}{DEZ=20cviM@Qc422mtpJ!C75GcV2JvBmCjBi_SSXEMIy@u(3gUo@I~!pl;zq<TFb'
        '`Hhy@uE=NH9T6viifF|nui5+ei?!*s>7N#FL134sX&iJgIVrx2<qy!Y8dc=?tOO$ThXOgS&r@zxJ7{`8CT)WqjCkZ)lmy$6@K>W$'
        'Y>RkQyZhWukh-CWwo_TG9mnDxhuwNmvXEcSPhKq-qG^pKyj!PN&}ix>MXSgkb(0hp;IUs{=<Tc{kL5=^W1b?v+x3-K<p0{TV_82I'
        '^S<Z?5R2JS3FEO~JY}gAELDA`y81Te(Y9c-<>-zG)$X~5^O}f!6(<ZXVdfp?Lxh;egE_XN-_9p};RW5m8}1QAdeM$bQ`KXA9;ajb'
        'K%F=ZqHWfVG2oVnRkhiK<r2xmkVPtGSt3~AizvkaxSjEi+7ayh3opO)a-)DbP8oyCC-Wx`@OT{aL6JZ98pl&SxuQ+ENKePnEke=5'
        'P8QwFu6%ZFMt()k%5$)OeiVM}b1z5-#oB-Khpl7WE<tJHyr<Tt$)RTU-EJpLiu|ck(xGc1bUOaK$nU=tq(<H?{IrthUvgEy$k{=Q'
        'B!gZ@g#mE!$hzn$*dax*Z1zRWQx(@^)RO@MKrZJemQ>{NR74YplF~FX77>LO#vj|r!VrMiH}YP0hliOceqPM3&AgX%<cc-MDrP;_'
        'A}F*(U!=i7BHeU*d=I9@gm3AGvR$sF?biz;gb3YW*!rhO@*@;eS;%Sr+BA)wdT(vU{LK({Vz195%@!M3M?j+Ma0_3bnvtDJGh`RT'
        'XfMRsQNS1!l@gCVn}4#%5^x6)Ts>w<*6)V_q9;`v>lVKa*2a&nihBq<{6=(OG-5N=_GLj*j;x^HaA-;y^TR;!RTTxP#5@f&HVfiW'
        'i0U9cH^;=DC;B?HQoU=4K*q1HIgHJ-rOoyA#f@e6QuFfahP$=7(tdrh)pW02U0!TADSjT$XW)F=xB?i0sRrWX75HJ2W953S=2m;L'
        ')h5H-Zi$XkhF>&^I~yt`aiM&odXu#3@c~n@{zKYPRtbotaHn~K=tRXnEKG*wHw6>juJF=}Of<F|bF9lf;ATL>fp}mff3l1Q_#02j'
        ';UjE4)6%BrVW}kM9PP$f2Tu`_Gb{EU@AG?Jx^UtAg@WQ%L!tLsW_hSI%hk=-n=N;9WrYm$=9bJ-cyKqWY;%!yvlu^O#yt;WvfaS)'
        'Tt_e@-y{G-u?%b%>N$P2i?Q%K@~38L?%iZi4dTlktB3r)5%|SJ2>j%oaUq}m_OG0&sY_zp@_M4W=`Q7wtdArKxniZo&l19&&EVYt'
        'eA^OS<9~>8xcR0?G=yzRI8#N?84GBgeM}4tqsvoK%7Z8|mf)!@!z>cJLy3YOM}DEb={3wq1`ieY$y@^?J&GBur!$WZQ^ahPI!5@k'
        '9(Rc;dnRbK+0m;QSnE(!n!YHWlU?37QpPHTs#Z<24H1Adl%nA{*ZP<f3mvt%)1!yxnyZUEYwRt~8K4MaSF-=E6dFZAO5mt~qYYqv'
        '<{aR&23zeKEils;$avtVUb)0voyW|kFlj7qAo>J7fEQF$deRYbtjJNmNLX1(SjZp>p=Uy>cq4l1aXJC8Srg8e7MESnNxR8{ZWSt;'
        'C9@bwCk+RVist<+9cVV?;9VajfuYqntIQars1LB&4pxUi+NR)s@Cd}pqJ(#$AFYrmD1rI|mOz;^hG|UWVGO4aFb8vY`M_Ak`U1s?'
        '%79r^BC%n;awaWZGMKhh30A_<oRdW%jjAtYsw`;Hqe9DK3p<#s0I4;u12ZW>Tv(u6_my&X1R;3{{5c0s*p-1Nu>%!Qb~J*_BrD?_'
        'pKV=RT54`>X~`+vf+!PuF9ik1aN}s)2;%9OT*Q=yAg1}+n+a8)UYPl1RM}=hlq-!|QDX}!5yS?M)&y}hI(TXXG5Vs2OuE>tv@`-c'
        'h<4P?&mF+nsV}gm9}a5tO0ONVu3evS(nV=AV6**DkmX|0wOL3Kvv?U5h$iZh-;E=vZD3UU=|?@Cm?M+@X&i8ZG(gzQ5>ORj=e#bB'
        '7i+`{DU275ef)`#L$=ckQ5(T#jRr)YXXwEhioAL=^{N06JJ9-^0|nMMmz(26-(Xiimzon-ov1C8Th(9#6x4PU+#<Y@k$NgYIWPbm'
        'dN%7xzM~ndielP4h=DAu6_%b%Xb6~=c9@ikoLL)Iy4294zy#GGiPTE;+$YmQEHIrZ^2x$HDMQOdNn{q0!M2>|J3I(^CkRpMmvWQq'
        ')&mb1M5uu3LuyF0cC^(H?vU8Vj?t(a#62yIE_j3)kx(xtbiZ4%BMr8kS50y>VQEewNky+Ce4X1+bLnVDmf&FufNV<}l2A8R+>^re'
        'epPyazPlm}&mjdwMsCu3&e^TtIB9iqW)?*-puwaDAHoUjhk-i*H&5XMO2m_)V)5G%&LkL;V4;G8cw)QAvCZ|~VuvWdOUz@eJ0FXX'
        'LZ!y}4(VHEjf%e;Yz0^qdz`#KS7w<p-tWTUv{>Yi3ju|wM5A9L5S()=TGmFHsM|1y8jCe-fbcL;`=TTuF6@m$jG{iRtk0?A@Jwi$'
        '5}PUozpju4;xNi6{QG<)^;EV)sl_#c%_bSrh4lcrZ+>;TtYmC8Qktg1bFKEG`s^HV?Hm9j(-WoSD$iC(l<bIjP2tT@Eio`9<?Cu+'
        '4@Fj0IF!ATA(}}g@cBcOz$eNQcx7>^z1ez$TAHSAXg+S4tW+A}X<bKjgYC@Ld%6m@WLdT%sA_l?rlqqIHcP=?b~d&u0D&xLqMVvV'
        'o`|W!1;dmDU9AO5%GqG5Z4rq$@C;XCOOaGnNC<o<M0{SYftqNY7Y<>alcjZ<>&@2X=El++sL(dAl6iiyq*F${(CVRxq>LS+QX+08'
        'J*e6u-b%}U#)?J}uwt8_VF_(oLCpeqzP}k7+NG>bVIRYuSa6cI&mThD)1|i15s`bf+1gs&YBx99rYzl}hG^-osi~2+2AzpM*&IfU'
        'rS;fwX-VXx*crAr`lQ4ZjfS@SbgYR4f;rl5iBtAFsD5`8;*|o8HbB%h*oLmU_2J&Iu!Ce2lKYloJWCa&Xb*$oCDj3OSBC~VCjmlE'
        'y%C`zi*5rAXxfBniZJEQ1j%}$N0BhH6A?-zh+laO8h#aWf=T9dqIDvz0l7ZZ5v30}5EZ6VN8+7hqjjtvQ9FJqvkEnr=+Q2JMwB?Z'
        'W)vgs*2qzVh>|R>)!|xIVjgm;UuB@m-@Xz_^mIC`Du&8Cl?yy!y+Q*fLiM={sv>`+c989M2Ii2QAp4AbLf(+`GM172vHX$znS59N'
        'Qhp$REkBgMksoFGeXcL40w-E8-pL<yyTP9DUCKIc;1?VDLvErn(1c5b?Gj-Z`41K(Jh6}jA>6WXE9>yRg@pIj_CiVW3#n3JvH)=i'
        '2Cm8P3;nEvG~~u&JJWe&cy^vF*db)0g%{6X7(dj19{-vl1+<ksfhZIxuC4frw?Q($T^)%on}Et7vw_ca?+NlD8;_JypdalMYDvb<'
        '!yC>bA$i}K6a|v%8|YnRK|`Q1rL4c50dD}5i7#M{4*g8+g8(td)POM@`wjVuaqQB_vFEX?+^3#s-*G424#%yTsT*{_I(+(Zbyq(P'
        'J^o(O$!B0Ty>78Kozb!8amn#t2ZQJgQ(iWQosUbtetc&5_>;AnY{GMM<SCEKhvW%)l7x5ySc`zOcY(1F<wrvP{_~(v{^1?@#|`->'
        '`DghT_)-2fKjMl#BBEmb`qBI(Fls&+#jX@o7wkJUXCUUU8)BYl(7K`OMq#7J&2QMd@2t;FPdrSP*Ee8->qp51<?(N#ZJ`ZEFK<tH'
        'sn4Mwbj#BXEB+C?n<MYHcgOOxcl@wrrWZqdpPG=QX6i}mUSjerp%i?oZ4Owd;3z+{n4(XA6X|`{QV&vEySC-puA7!*TP8U(T_~Hp'
        'N_<b$ty|(T;+lT$&iQrXek+TsSFW|_d@;Ycq=}g#%;a_5O@mTJLM0DXf*v(vUNubD(A3rV<Dxu&2vJU0Q8qT)?&7uftDCLWH=D~O'
        '(b;7Y(UFU9Dm0yvh)Oc_R<ZqxGQRT*huHaHyEC13*?NPvJ>MQVDyfw>r1Z^*j*nGr3{^7ExESXTA;zOMF|IDQ7T25YW{U**rv3s^'
        'e$l8M!<z2LX4&DvRw6=kC|G`u924rrLkM-eCX_C@NTAE@S`}p~Ni~*ywORUfe3p*)(!&%#F4%?t11_r@u+qlj6}Q=HZEAC^kaV>('
        'U{h%5Lk%4^Liayes!tdrvDY`oqArta4CQIf_6hgWuof_k`)~Q_jk~6&rsRKaJb*tpj?(3Ex;#pkvvfI4mj+#)q03k4a)B<(ba@4r'
        'abnJ=4#-!NGmie2SEh~`B$|Dh<DWw&`xK%ctpq$>iFKhA<_p#A#uZxfZ|k?G<=?-+w6gZx9kL4cJ~*p<I6XP50BxrZP8kz3#SH!5'
        '0G2xnt9t#LxcmnO%*0i)DMuIw+(^lWF<o})l2z7R|J}5)=R1_bvrglGFz2DjJ|X}B'
    )
    assert isinstance(_MODEL_, _pydsdl_.ServiceType)
