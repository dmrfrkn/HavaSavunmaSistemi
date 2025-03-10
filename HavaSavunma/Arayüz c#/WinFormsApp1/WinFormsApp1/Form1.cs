namespace WinFormsApp1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            // Kamera Görüntüsü
            PictureBox cameraView = new PictureBox
            {
                Size = new Size(400, 300),
                Location = new Point(10, 30),
                BorderStyle = BorderStyle.FixedSingle,
                BackColor = Color.Black
            };
            this.Controls.Add(cameraView);

            // Log Alaný
            TextBox logBox = new TextBox
            {
                Size = new Size(200, 300),
                Location = new Point(420, 30),
                Multiline = true,
                ScrollBars = ScrollBars.Vertical
            };
            this.Controls.Add(logBox);

            // Ateþ Etme Kontrolü
            TrackBar fireSlider = new TrackBar
            {
                Minimum = -30,
                Maximum = 90,
                Location = new Point(10, 340),
                Width = 150
            };
            this.Controls.Add(fireSlider);

            Button fireButton = new Button
            {
                Text = "Fire",
                Location = new Point(170, 340)
            };
            this.Controls.Add(fireButton);

            // Hareket Kontrolü
            TrackBar moveSlider = new TrackBar
            {
                Minimum = -30,
                Maximum = 30,
                Location = new Point(10, 380),
                Width = 150
            };
            this.Controls.Add(moveSlider);

            Button moveButton = new Button
            {
                Text = "Move",
                Location = new Point(170, 380)
            };
            this.Controls.Add(moveButton);

            // Mermi Sayacý
            Label bulletLabel = new Label
            {
                Text = "Bullets: 61",
                Location = new Point(10, 420),
                AutoSize = true
            };
            this.Controls.Add(bulletLabel);

            // Timer Butonu
            Button timerButton = new Button
            {
                Text = "Timer",
                Location = new Point(170, 420)
            };
            this.Controls.Add(timerButton);

        }

    }
}