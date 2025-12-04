return {
	"barrett-ruth/live-server.nvim",
	cmd = { "LiveServerStart", "LiveServerStop" },
	config = true,
	keys = {
		{
			"<leader>ls",
			"<cmd>LiveServerStart<cr>",
			desc = "Start Live Server",
		},
		{
			"<leader>lx",
			"<cmd>LiveServerStop<cr>",
			desc = "Stop Live Server",
		},
	},
}
