import re
import typing

import inflection

# import wordninja

from .utils import dedupPreservingOrder

__all__ = ("canonicalizeOrigName", "convertName")

numUnderscoreSeparatedStr = re.compile(r"([h-zH-Z]+[a-zA-Z]+|[a-zA-Z]+[h-zH-Z]+)_(\d)$")
allowedKSIdRx = re.compile(r"^\w+$")


def attachNumber(s: str) -> str:
	return numUnderscoreSeparatedStr.subn("\\1\\2", s)[0]


W_POSTFIX = "_W"
A_POSTFIX = "_A"


def clearPostfixes(n: str) -> str:
	if n.endswith(W_POSTFIX):
		n = n[: -len(W_POSTFIX)]
	elif n.endswith(A_POSTFIX):
		n = n[: -len(A_POSTFIX)]
	return n


def canonicalizeOrigName(n: str) -> str:
	"""Removes unneeded prefixes and postfixes from `-orig-id`s"""
	if n.startswith(PR_TAG):
		n = clearPostfixes(n)
	return n


PID_TAG = "PidTag"
PTAG = "ptag"
PR_TAG = "PR_"
INT_SCH_TAG = "InternalSchema"

filters = {
	PR_TAG: (
		("_OAB_", "_OFFLINE_ADDRESS_BOOK_"),
		("EMSMDB", "EMS_MDB"),
		("EMS_AB_", "ADDRESS_BOOK_"),
		("ADDRTYPE", "ADDR_TYPE"),
		("ORADDRESS", "OR_ADDRESS"),
		("_ADDR_", "_ADDRESS_"),  #
		("_AUTH_", "_AUTHORIZED_"),
		("_DELIV_", "_DELIVERY_"),
		("STOREEID", "STORE_EID"),
		("_SVREID", "_SVR_EID"),
		("ABEID", "ADDRESS_BOOK_EID"),
		("SEQID", "SEQ_ID"),
		("DRAFTID", "DRAFT_ID"),
		("SRCHID", "SRCH_ID"),
		("OFLID", "OFL_ID"),
		("_EID", "_ENTRY_ID"),
		("ENTRYID", "ENTRY_ID"),
		("LINKID", "LINK_ID"),
		("REPLACETIME", "REPLACE_TIME"),
		("TRACKSTATUS", "TRACK_STATUS"),
		("CLIENTID", "CLIENT_ID"),
		("PARENTID", "PARENT_ID"),
		("SPLUS", "SCHD_PLUS"),
		("ENABLEDON", "ENABLED_ON"),
		("ONSERVER", "ON_SERVER"),
		("_HAB_", "_hier_"),
		("SCHDINFO_", "schd_info_"),
		("_FREEBUSY_", "_free_busy_"),
		("_DL", "_distr_list"),
		("_MTSOUT_", "_MTS_OUT_"),
		("_MTSIN_", "_MTS_IN_"),
		("_MHS_", "_MESSAGE_HANDLING_SYSTEM_"),
		("_MTA", "_MESSAGE_TRANSFER_AGENT"),
		("_RECKEY", "_RECORD_KEY"),
		("XMLSTREAM", "XML_STREAM"),
		("WB_SF_", "WB_SEARCH_FOLDER_"),
		("_CONT_", "_CONTENT_"),
		("CONTAINERID", "CONTAINER_ID"),
		("TEMPLATEID", "template_id"),
		("PROPOSEDENDTIME", "PROPOSED_END_TIME"),
		("PROPOSEDSTARTTIME", "PROPOSED_STARTTIME"),
		("STARTTIME", "START_TIME"),
		("CONTACTPHOTO", "CONTACT_PHOTO"),
		("FREEBUSY", "FREE_BUSY"),
		("SENDPOST", "SEND_POST"),
		("READPOST", "READ_POST"),
		("REPORTNOTE", "REPORT_NOTE"),
		("SENDNOTE", "SEND_NOTE"),
		("READNOTE", "READ_NOTE"),
		("ENDTXT", "END_TXT"),
		("BEGINTXT", "BEGIN_TXT"),
		("BODYTAG", "BODY_TAG"),
		("MIGRATEPROFILE", "MIGRATE_PROFILE"),
		("CHANGENUM", "CHANGE_NUM"),
		("VERSIONHISTORY", "VERSION_HISTORY"),
		("VERSIONSKELETON", "VERSION_SKELETON"),
		("SERVERID", "SERVER_ID"),
		("SUBITEMID", "SUBITEM_ID"),
		("INETMAIL", "INET_MAIL"),
		("_EID", "_ENTRY_ID"),
		("DOTSTUFF", "DOT_STUFF"),
		("NEWSFEED", "NEWS_FEED"),
		("PERUSER", "PER_USER"),
		("MAILBEAT", "MAIL_BEAT"),
		("HOTSITE", "HOT_SITE"),
		("ENDTIME", "END_TIME"),
		("FIXFONT", "FIX_FONT"),
		("CCWRAP", "CC_WRAP"),
		("METATAG", "META_TAG"),
		("ICONURL", "ICON_URL"),
		("ITEMPROC", "ITEM_PROC"),
		("VIEWINFO", "VIEW_INFO"),
		("DISPLAYNAME", "DISPLAY_NAME"),
		("FXSRCSTREAM", "FX_SRC_STREAM"),
		("FXDESTSTREAM", "FX_DEST_STREAM"),
		("OTHERMAILBOX", "OTHER_MAILBOX"),
		("VIEWPRIVATE", "VIEW_PRIVATE"),
		("FOLDERTYPE", "FOLDER_TYPE"),
		("VIEWTYPE", "VIEW_TYPE"),
		("OSTID", "OST_ID"),
		("SHAREDDATA", "SHARED_DATA"),
		("NOTFOUND", "NOT_FOUND"),
		("MAPIUID", "MAPI_UID"),
		("MAPIFORM", "MAPI_FORM"),
		("PHONEBOOK", "PHONE_BOOK"),
		("TESTCLSID", "TEST_CLSID"),
		("LABELEDURI", "LABELED_URI"),
		("DISPNAME", "DISP_NAME"),
		("SYNCEVENT", "SYNC_EVENT"),
		("SLOWLINK", "SLOW_LINK"),
		("DIALUP", "DIAL_UP"),
		("WAITFOR", "WAIT_FOR"),
		("MIMEWRAP", "MIME_WRAP"),
		("LOGLEV", "LOG_LEVEL"),
		("TCPIP", "TCP_IP"),
		("VRFY", "VERIFY"),
		("TRACEINFO", "TRACE_INFO"),
		("SPAMTYPE", "SPAM_TYPE"),
		("USERFIELDS", "USER_FIELDS"),
		("VIEWLIST", "VIEW_LIST"),
		("CLEARPROPS", "CLEAR_PROPS"),
		("LOGFILE", "LOG_FILE"),
		("DELTAX", "DELTA_X"),
		("DELTAY", "DELTA_Y"),
		("XPOS", "X_POS"),
		("YPOS", "Y_POS"),
		("MAILFROM", "MAIL_FROM"),
		("DATAINIT", "DATA_INIT"),
		("DATATERM", "DATA_TERM"),
		("_HDRS_", "_HEADERS_"),
		("OUTQ_", "OUT_Q_"),
		("INQ_", "IN_Q_"),
		("DATABLOCK", "DATA_BLOCK"),
		("VIEWFLAGS", "VIEW_FLAGS"),
		("SAVEAS", "SAVE_AS"),
		("FOLDERID", "FOLDER_ID"),
		("PORTNO", "PORT_NO"),
		("BIFINFO", "BIF_INFO"),
		("MSGTRACKING", "MSG_TRACKING"),
		("AUTORESPONSE", "AUTO_RESPONSE"),
		("FAVFLD", "FAV_FLD"),
		("BODYPART", "BODY_PART"),
		("LISTINFO", "LIST_INFO"),
		("reqcn", "req_cn"),
		("REQNAME", "REQ_NAME"),
		("INSADMIN", "INS_ADMIN"),
	),
	PID_TAG: (
		("security_descriptor", "nt_security_descriptor"),
		("attribute_", "attr_"),
		("access_control_list_", "acl_"),
		("schedule_", "schd_"),
		("_distribution_list", "_distr_list"),
		("_unauthorized_", "_unauth_"),
		("appointment", "appt"),
		("hierarchical", "hier"),
		("msgid", "msg_id"),
		("itemid", "item_id"),
		("changenum", "change_num"),
		("_away", "OOF"),
		("attachlist", "attach_list"),
		("temporaryflags", "temporary_flags"),
		("errorinfo", "error_info"),
		("msgsize", "msg_size"),
		("_t_bl_", "_table_"),
		("replid", "repl_id"),
	),
	None: (
		("address", "addr"),
		("addrbook", "addr_book"),
		("rootdir", "root_dir"),
		("message", "msg"),
		("msgclass", "msg_class"),
		("mtsid", "mts_id"),
		("sentmail", "sent_mail"),
		("hasattach", "has_attachments"),
		("_extended", "_ex"),
		("_eid", "_entry_id"),
		("_telephone_", "_phone_"),
		("received_", "rcvd_"),
		("number", "num"),
		("_object_", "_obj_"),
		("to_do_", "todo_"),
		("_message_", "_msg_"),
		("internet", "inet"),
		("acct", "account"),
		("maximum", "max"),
		("minimum", "min"),
		("transmitable", "transmittable"),
		("subfolder", "sub_folder"),
		("rowid", "row_id"),
		("_binary", "_bin"),
		("recurrenceid", "recurrence_id"),
		("readonly", "read_only"),
		("pathname", "path_name"),
		("templateid", "template_id"),
		("_mid_", "_msg_id_"),
		("datatype", "data_type"),
		("codepage", "code_page"),
		("dam_", "deferred_action_message_"),
		("_replid", "_repl_id"),
		("webviewinfo", "webview_info"),
		("webview", "web_view"),
		("mailuser", "mail_user"),
		("_cpid", "_codepage_id"),
		("longterm", "long_term"),
		("newsfeed", "news_feed"),
	),
}


def processFilterBank(s, bank):
	for f in bank:
		s = s.replace(*f)
	return s


wordninjaFalsePositives = (
	"corre_lat_or",
	"e_its",
	"in_it",
	"i_pms",
	"rec_ip",
	"i_pm",
	"x_400",
	"a_ddr",
	"re_pl",
	"rc_vd",
	"a_ppt",
	"tn_ef",
	"ds_a",
	"fr_eq",
	"a_lg",
	"auto_reply",
	"time_out",
	"a_ck",
	"re_cv",
	"rcp_t",
	"canonical_iz_ation",
	"map_i",
	"tn_s",
	"e_smtp",
	"e_trn",
	"s_mime",
	"synchronize_r",
	"rt_f",
	"acc_t",
	"gui_d",
	"mid_set",
	"x_mt",
	"sch_d",
	"spool_er",
	"nts_d",
	"n_td_n",
	"s_rc",
	"s_can",
	"de_st",
	"i_mail",
	"rm_q",
	"x_ref",
	"t_bl",
	"ow_a",
	"at_tr",
	"p_1",
	"u_id",
	"cl_sid",
	"out_box",
	"m_db",
	"as_soc",
	"p_2",
	"pre_c",
	"loop_back",
	"re_calc",
	"de_queue",
	"m_gr",
	"au_th",
	"start_tls",
	"ku_lane",
	"dia_g",
	"d_is_tr",
	"n_ntp",
	"if_s",
	"an_r",
	"c_dorm",
	"c_doo_or",
	"cd_of_bc",
	"s_vr",
	"transmit_able",
	"tty_tdd",
	"pa_b",
	"a_cl",
	"du_a",
	"ad_atp_3",
	"con_v",
	"p_km",
	"version_ing",
	"l_cid",
	"in_cr",
	"re_q",
	"rg_m",
	"c_pid",
	"fl_d",
	"ex_ch_50",
	"mb_in",
	"addr_s",
	"o_of",
	"sr_ch",
	"o_ab",
	"of_l",
	"open_ning",
	"encrypt_er",
	"fa_v",
	"m_sdos",
	"dx_a",
	"roll_over",
	"back_off",
	"de_sig",
	"una_u_th",
	"x_121",
	"xm_it",
	"l_dap",
	"cf_g",
	"adr_s",
	"mt_s",
	"pui_d",
	"mon_the_s",
	"x_view",
	"log_on",
	"cate_g",
	"back_fill",
	"in_st",
	"de_liv",
	"appt_s",
	"del_s",
	"reqc_n",
	"telet_ex",
)
wordninjaFalsePositives = [(el, el.replace("_", "")) for el in wordninjaFalsePositives]


def fix_after_wordninja(n):
	return processFilterBank(n, wordninjaFalsePositives)


def convertName(n: str) -> str:
	"""Tries to normalize a name the way that different kinds of source names result into the same name. Also tries to make the name more easy to read"""

	sprt = n.startswith(PR_TAG)
	if sprt:
		n = n[len(PR_TAG) :]
		n = processFilterBank(n, filters[PR_TAG])
		n = attachNumber(n)
	elif n.startswith(PID_TAG):
		n = n[len(PID_TAG) :]
	elif n.startswith(PTAG):
		n = n[len(PTAG) :]
		n = n.replace("MTA", "MessageTransferAgent")
	elif n.startswith(INT_SCH_TAG):
		n = n[len(INT_SCH_TAG) :]

	if not sprt:
		n = inflection.underscore(n)
		n = processFilterBank(n, filters[PID_TAG])

	n = n.lower()
	if "attachment" not in n:
		n.replace("has_attach", "has_attachments")

	# n = fix_after_wordninja("_".join(wordninja.split(n)))

	n = processFilterBank(n, filters[None])

	return n


def selectAndConvertNamesAdmissibleToId(origIds):
	for el in origIds:
		if allowedKSIdRx.match(el):
			yield convertName(el)


def prepareNamesAndOrigIds(origIds, sort=True):
	origIds = list(dedupPreservingOrder(canonicalizeOrigName(el) for el in origIds))
	names = selectAndConvertNamesAdmissibleToId(origIds)
	if sort:
		names = sorted(set(names))
	else:
		names = dedupPreservingOrder(names)

	return origIds, names
