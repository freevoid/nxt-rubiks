%.rxe: %.nxc
	nbc $< -O=$@

bridge: bt_bridge.rxe
	nxt_push bt_bridge.rxe

bt_bridge.rxe: bt_bridge.nxc rotate.nxc
	nbc $< -O=$@


